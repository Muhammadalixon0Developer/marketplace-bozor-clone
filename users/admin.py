from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group

admin.site.register(Saved)
admin.site.register(CustomUser)
admin.site.unregister(Group)
