import os

from django.conf import settings


def user_avatar_upload_path(instance, filename):
    ext = os.path.splitext(filename)[1]
    file_name = f'avatar{ext}'
    file_path = f'users/{instance.public_id}/{file_name}'
    full_path = os.path.join(settings.BASE_DIR, file_path)

    if os.path.isfile(full_path):
        os.remove(full_path)

    return file_path
