from django.conf import settings
from django.utils import functional


# my class and functional
from profiles.utils import getRandomCode


# third party
import datetime
import os


def userPostPath(instance, filename):
    dt = str(datetime.datetime.today()).split()[0]
    post_name = f'posts/user_{instance.author.user.id}_{instance.author}/{dt}/{filename}'
    full_path = os.path.join(settings.MEDIA_ROOT, post_name)

    ex = os.path.exists(full_path)
    while ex:
        random = getRandomCode()
        post_name = f'posts/user_{instance.author.user.id}_{instance.author}/{dt}/{random}{filename}'
        full_path = os.path.join(settings.MEDIA_ROOT, post_name)
        ex = os.path.exists(full_path)

    return post_name
