from django.contrib import admin

# Register your models here.
from .models import *


class Admin_(admin.ModelAdmin):
    readonly_fields = (
        'updated',
        'created',
    )


admin.site.register(Post, Admin_)
admin.site.register(Comment, Admin_)
admin.site.register(Like, Admin_)
