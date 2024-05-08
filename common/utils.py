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


def snake_to_camel(snake_str):
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])

def camel_to_snake(camel_str):
    snake_chars = []
    for i, char in enumerate(camel_str):
        if i > 0 and char.isupper():
            snake_chars.append('_')
        snake_chars.append(char.lower())
    return ''.join(snake_chars)

def delete_old_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)

def validate_image_size(value):
    filesize = value.size
    
    if filesize > 2 * 1024 * 1024:  # 2MB
        raise ValidationError("The maximum file size that can be uploaded is 2MB")
