from django.core.exceptions import ValidationError

def validate_image_size(value):
    filesize = value.size
    
    if filesize > 2 * 1024 * 1024:  # 2MB
        raise ValidationError("The maximum file size that can be uploaded is 2MB")