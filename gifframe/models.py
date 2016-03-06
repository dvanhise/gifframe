from django.db import models
from base58 import b58encode

BASE = 1000


class Cachable(models.Model):

    link = models.URLField(unique=True)
    externalId = models.CharField(max_length=100, blank=True)
    height = models.IntegerField()
    width = models.IntegerField()
    views = models.IntegerField(default=1)

    def __str__(self):
        return self.link

    def delete(self, using=None):
        self.frame_set.all().delete()
        super(Cachable, self).delete(using)

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
        return self.gif[50:] + ' - ' + self.order
