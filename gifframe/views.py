import urllib.request
import uuid
from PIL import Image
from io import BytesIO
import os.path as path
from urllib.parse import urlparse

from django.shortcuts import render, redirect
from django.views.generic import View
from django.core.exceptions import ObjectDoesNotExist
from boto.s3.key import Key
from boto.s3.connection import S3Connection, OrdinaryCallingFormat

from .settings import BASE_DIR, MAIN_BUCKET, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
from .models import Frame, Cachable

# test gif: https://upload.wikimedia.org/wikipedia/commons/8/83/Utah_Territory_evolution_animation_-_August_2011.gif
# http://i.imgur.com/YTMYqQP.gif
# http://i.imgur.com/foxwpvR.gif

# get access to this http://images.gifframe.test.s3.amazonaws.com/aa4f1a0c-082b-4b4f-9cb4-784a344a0f54.png
MAX_HEIGHT = 800
MAX_WIDTH = 1000


class IdFrameView(View):
    requestType = 'id'

    def get(self, request, gifId):
        context = checkCache(gifId)
        if not context:
            return renderError(request, 'The id ({}) was not found'.format(gifId))

        context['imageRoot'] = 'http://{}.s3.amazonaws.com/'.format(MAIN_BUCKET)
        return render(request, 'page.html', context)


class UrlFrameView(View):
    def get(self, request, gifUrl):
        url = urlparse(gifUrl)
        print('<<url parse>> ' + str(url))

        if not url.path.endswith(('.gif', '.gifv')):
            return renderError(request, 'Link did not appear to be a gif')

        # gifUrl = '//{}{}'.format(url.netloc, url.path)
        # gifUrl = re.sub(r'/$', '', gifUrl, re.I)

        # FIXME: The vulnerability of e.g. ___imgur.com being matched
        SITES = ['imgur.com', 'wikimedia.org', 'gfycat.com', 'photobucket.com']
        # re.match(r'^([^\s/]+\.)?a', url.netloc)
        if not len([domain for domain in SITES if domain in gifUrl]):
            return renderError(request, 'Link is not from a supported site')

        # Check cache for url
        try:
            cache = Cachable.objects.get(link__iexact=gifUrl)
            return redirect('idFrames', gifId=cache.externalId)
        except ObjectDoesNotExist:
            context = parseGif(gifUrl)

        if not context:
            return renderError(request, 'Unable to read file as a gif')
        context['imageRoot'] = 'http://{}.s3.amazonaws.com/'.format(MAIN_BUCKET)
        return render(request, 'page.html', context)


class ResetFrameView(View):

    def get(self, request, gifId):
        try:
            cache = Cachable.objects.get(externalId=gifId)
        except ObjectDoesNotExist:
            return renderError(request, 'The id ({}) was not found'.format(gifId))

        # TODO:  delete s3 links
        # delete cache
        # keep same external id
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
        'frames': frames,
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
    print('<<log>> Image location ' + str(location))
    try:
        im = Image.open(
            BytesIO(urllib.request.urlopen(location).read())
        )
    except OSError:
        return {}

    print('<<log>> image ' + str(im))
    # Validate file
    if im.format.lower() != 'gif':
        return None

    width, height = im.size
    # Rezise image if necessary
    if height > MAX_HEIGHT:
        ratio = MAX_HEIGHT/height
        if width * ratio > MAX_WIDTH:
            ratio = MAX_WIDTH/width
        width = int(width*ratio)
        height = int(height*ratio)
        im.thumbnail((height, width), Image.ANTIALIAS)

    cache = Cachable(link=location, height=height, width=width)
    cache.save()

    conn = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, calling_format=OrdinaryCallingFormat())
    bucket = conn.get_bucket(MAIN_BUCKET)
    k = Key(bucket)
    if not k:
        print('<<error>> Couldn\'t connect to bucket ' + MAIN_BUCKET)
        return None

    # Iterate through gif and save frames
    frames = []
    count = 0
    try:
        while 1:
            count += 1
            if count >= 200:
                break

            print('<<log>> frame #' + str(count))
            frameKey = str(uuid.uuid4()) + '.png'
            imgPath = path.join(BASE_DIR, 'static', 'images', frameKey)

            im.save(imgPath, 'png')
            print('<<log>> Saving to ' + str(imgPath))
            k.key = frameKey
            k.set_contents_from_filename(imgPath)
            # TODO: delete local file or find a way to not have to save it locally
            frames.append(frameKey)
            Frame(image=frameKey, order=len(frames), gif=cache).save()
            im.seek(im.tell()+1)
    except EOFError:
        pass

    if not frames:
        print('<<log>> No frames were saved')

    return {
        'source': location,
        'frames': frames,
        'height': height,
        'width': width,
        'externalId': cache.externalId
    }
