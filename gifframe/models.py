from django.db import models
from base58 import b58encode
from .settings import MAIN_BUCKET, AWS_CONNECTION

BASE = 345


class Cachable(models.Model):

    # TODO: Create lookup for determining if two urls are equivalent
    link = models.URLField(unique=True)
    externalId = models.CharField(max_length=100, unique=True, blank=True)
    height = models.IntegerField()
    width = models.IntegerField()
    views = models.IntegerField(default=1)

    def __str__(self):
        return self.link

    def delete(self, using=None):
        self.deleteFrames()
        super(Cachable, self).delete(using)

    def deleteFrames(self):
        frames = self.frame_set.all()
        if frames.exists():
            conn = AWS_CONNECTION
            bucket = conn.get_bucket(MAIN_BUCKET, validate=False)
            bucket.delete_keys(frames.values_list('image', flat=True))
            frames.delete()

    def save(self, *args, **kwargs):
        updated = self.id
        super(Cachable, self).save(*args, **kwargs)

        # Generate an externalId if the object was just created
        if not updated:
            self.externalId = b58encode(bytearray(str(BASE + self.id), 'utf8'))
            self.save()


class Frame(models.Model):

    image = models.CharField(max_length=200)
    order = models.IntegerField()
    gif = models.ForeignKey('Cachable')

    class Meta:
        unique_together = ('order', 'gif')

    def __str__(self):
        return self.gif.link[50:] + ' - ' + str(self.order)
