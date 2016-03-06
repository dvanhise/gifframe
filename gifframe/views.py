import urllib.request
import re
import uuid
from PIL import Image
from io import BytesIO
import os.path as path
from urllib.parse import urlparse

from django.shortcuts import render, redirect
from django.views.generic import View
from django.core.exceptions import ObjectDoesNotExist
import boto
from boto.s3.key import Key

from .settings import BASE_DIR, MAIN_BUCKET
from .models import Frame, Cachable

# test gif: https://upload.wikimedia.org/wikipedia/commons/8/83/Utah_Territory_evolution_animation_-_August_2011.gif
MAX_HEIGHT = 800
MAX_WIDTH = 1000


class IdFrameView(View):
    requestType = 'id'

    def get(self, request, gifId):
        context = checkCache(gifId)
        if not context:
            return renderError(request, 'The id ({}) was not found'.format(gifId))

        return render(request, 'page.html', context)


class UrlFrameView(View):
    def get(self, request, gifUrl):
        # Trim down the url, remove http, www, and trailing slash
        url = urlparse(gifUrl)
        print('<<url parse>> ' + str(url))
        gifUrl = re.sub(r'^(https?://)?(www\.)?', '', gifUrl, re.I)
        gifUrl = re.sub(r'/$', '', gifUrl, re.I)

        if not url.path.endswith(('.gif', '.gifv')):
            return renderError(request, 'Link did not appear to be a gif')

        if not url.netloc:
            return renderError(request, 'Couldn\'t parse link in a meaningful way')

        # TODO: limit the sites that can be used
        # SITES = ['imgur.com', 'wikimedia.org', 'gfycat.com', 'photobucket.com']
        # re.match(r'^([^\s/]+\.)?a', url.netloc)

        # Check cache for url
        try:
            cache = Cachable.objects.get(link__iexact=gifUrl)
            return redirect('idFrames', gifId=cache.externalId)
        except ObjectDoesNotExist:
            context = parseGif(gifUrl)

        if not context:
            return renderError(request, 'Unable to read file as a gif')
        return render(request, 'page.html', context)


class ResetFrameView(View):

    def get(self, request, gifId):
        try:
            cache = Cachable.objects.get(externalId=gifId)
        except ObjectDoesNotExist:
            return renderError(request, 'The id ({}) was not found'.format(gifId))

        # TODO:  delete s3 links
        # delete cache
        context = parseGif(gifId)
        return render(request, 'page.html', context)


class HomeView(View):

    def get(self, request):
        return render(request, 'home.html')


def renderError(request, error):
    print('<<error>> ' + str(error))
    return render(request, 'page.html', {'error': error})


# On cache hit returns the correct context
# On cache miss returns None
def checkCache(gifId):
    try:
        cache = Cachable.objects.get(externalId=gifId)
    except ObjectDoesNotExist:
        return {}

    frames = cache.frame_set.all().order_by('order').values_list('image', flat=True)
    return {
        'source': cache.link,
        'frames': [path.join('images', f) for f in frames],
        'height': cache.height,
        'width': cache.width,
        'externalId': cache.externalId
    }


# Tries to grab a gif from 'location'
# Opens and validates with pillow
# Generates frames and saves them to s3
# Caches data in db
# Returns generated context
def parseGif(location):
    # Get the gif and open with pillow
    try:
        im = Image.open(
            BytesIO(urllib.request.urlopen(location).read())
        )
    except OSError:
        return {}

    # Validate file
    if im.format.lower() != 'gif':
        return {}

    height, width = im.size
    # Rezise image if necessary
    if height > MAX_HEIGHT:
        ratio = MAX_HEIGHT/height
        if width * ratio > MAX_WIDTH:
            ratio = MAX_WIDTH/width
        width = int(width*ratio)
        height = int(height*ratio)
        im.thumbhail((height, width), Image.ANTIALIAS)

    cache = Cachable(link=location, height=height, width=width)
    cache.save()

    conn = boto.connect_s3()
    bucket = conn.lookup(MAIN_BUCKET)

    k = Key(bucket)

    # Iterate through gif and save frames
    frames = []
    count = 0
    try:
        while 1:
            count += 1
            if count >= 200:
                break

            frameKey = str(uuid.uuid4()) + '.jpg'
            imgPath = path.join(BASE_DIR, 'static', 'images', frameKey)

            im.save(imgPath, 'jpg')
            k.set_contents_from_filename(imgPath)
            # TODO: delete local file or find a way to not have to save it locally
            frames.append(path.join('images', frameKey))
            Frame(image=frameKey, order=len(frames), gif=cache).save()
            im.seek(im.tell()+1)
    except EOFError:
        pass

    return {
        'source': location,
        'frames': frames,
        'height': height,
        'width': width,
        'externalId': cache.externalId
    }
