from django.contrib import admin

from .models import Cachable, Frame

admin.site.register(Cachable)
admin.site.register(Frame)
