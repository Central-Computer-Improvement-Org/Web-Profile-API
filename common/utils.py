import os

from datetime import datetime
from django.core.files.base import ContentFile

def rename_image_file(image, prefix):
    if image:
        new_image = ContentFile(image.read())
        timestamp = prefix + "-" + datetime.now().strftime('%Y%m%d%H%M%S')
        _, extension = os.path.splitext(image.name)
        new_image.name = f'{timestamp}{extension}'
        return new_image
    return image

def id_generator(prefix):
    return prefix + "-" + datetime.now().strftime('%Y%m%d%H%M%S')