from django.contrib import admin

# Register your models here.
from .models import *


class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = (
        'slug',
        'updated',
        'created',
    )


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Relationship)
