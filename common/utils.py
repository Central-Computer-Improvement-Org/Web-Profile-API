import os

from django.utils import timezone
from django.core.files.base import ContentFile

def rename_image_file(image, prefix):
    if image:
        new_image = ContentFile(image.read())
        timestamp = f'{prefix}-{timezone.now().strftime("%Y%m%d%H%M%S%f")}'
        _, extension = os.path.splitext(image.name)
        new_image.name = f'{timestamp}{extension}'
        return new_image
    return image

def id_generator(prefix):
    return f'{prefix}-{timezone.now().strftime("%Y%m%d%H%M%S%f")}'

def delete_old_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
