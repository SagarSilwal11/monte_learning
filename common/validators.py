# from django.core.exceptions import ValidationError

# def validate_name_length(value):
#     min_length=2
#     max_length=50
#     if len(value)< min_length:
#         raise ValidationError(f'Name must be at least {min_length} characters long.')
#     if len(value)> max_length:
#         raise ValidationError(f'Name must exceed {max_length} characters.')
from django.core.exceptions import ValidationError
import os

# ✅ Validate media type (must be "image" or "icon")
def validation_media(value):
    if value not in ['image', 'icon']:
        raise ValidationError("Media type must be either 'image' or 'icon'.")

# ✅ Validate image file type
def validate_file(value):
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp']
    ext = os.path.splitext(value.name)[1]
    if ext.lower() not in valid_extensions:
        raise ValidationError(f"Unsupported file type: {ext}. Allowed: {', '.join(valid_extensions)}")

# ✅ Validate name length
def validate_name_length(value):
    if len(value) < 3:
        raise ValidationError("Name must be at least 3 characters long.")
    if len(value) > 255:
        raise ValidationError("Name must not exceed 255 characters.")

# ✅ Validate image size (example: max 5MB)
def validate_image_size(value):
    max_size = 5 * 1024 * 1024  # 5MB
    if value > max_size:
        raise ValidationError("Image size must not exceed 5MB.")

# ✅ Validate alt text
def validate_alt_text(value):
    if value and len(value) > 255:
        raise ValidationError("Alt text must not exceed 255 characters.")

# ✅ Validate caption
def validate_caption(value):
    if value and len(value) > 500:
        raise ValidationError("Caption must not exceed 500 characters.")

    
def validate_name_length(value):
    min_length=2
    max_length=50
    if len(value)< min_length:
        raise ValidationError(f'Name must be at least {min_length} characters long.')
    if len(value)> max_length:
        raise ValidationError(f'Name must exceed {max_length} characters.')

