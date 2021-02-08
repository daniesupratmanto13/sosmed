from django.conf import settings

# third party
import uuid
import os


def getRandomCode():
    code = str(uuid.uuid4())[:8].replace('-', '').lower()
    return code


def userAvatarPath(instance, filename):
    avatar_pic_name = f'avatars/user_{instance.user.id}-{instance.user}/avatar_{filename}'
    full_path = os.path.join(settings.MEDIA_ROOT, avatar_pic_name)

    if os.path.exists(full_path):
        os.remove(full_path)

    return avatar_pic_name
