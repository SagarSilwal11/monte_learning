
from django.core.exceptions import ValidationError
import os

# ✅ Validate media type (must be "image" or "icon")
def validation_media(value):
    if value not in ['image', 'icon']:
        raise ValidationError("Media type must be either 'image' or 'icon'.")
# Validate file type for images 
def validate_image_file(value):
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    ext = os.path.splitext(value.name)[1]
    if ext.lower() not in valid_extensions:
        raise ValidationError(f"Unsupported image file type: {ext}. Allowed: {', '.join(valid_extensions)}")

# ✅ Validate file type for icons
def validate_icon_file(value):
    valid_extensions = ['.png', '.svg', '.ico']
    ext = os.path.splitext(value.name)[1]
    if ext.lower() not in valid_extensions:
        raise ValidationError(f"Unsupported icon file type: {ext}. Allowed: {', '.join(valid_extensions)}")

# ✅ Validate name length (common for both images and icons)
def validate_name_length(value):
    if len(value) < 3:
        raise ValidationError("Name must be at least 3 characters long.")
    if len(value) > 255:
        raise ValidationError("Name must not exceed 255 characters.")

# ✅ Validate file size for images (example: max 5MB)
def validate_image_size(value):
    max_size = 5 * 1024 * 1024  # 5MB
    if value > max_size:
        raise ValidationError("Image size must not exceed 5MB.")

# ✅ Validate file size for icons (example: max 1MB)
def validate_icon_size(value):
    max_size = 1 * 1024 * 1024  # 1MB
    if value > max_size:
        raise ValidationError("Icon size must not exceed 1MB.")


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

# ✅ Validate dimensions for images (example: max 1920x1080)
def validate_image_dimensions(file):
    from PIL import Image as PILImage
    file.open()
    image = PILImage.open(file)
    width, height = image.size
    if width > 1920 or height > 1080:
        raise ValidationError("Image dimensions must not exceed 1920x1080 pixels.")

# ✅ Validate dimensions for icons (example: max 64x64)
def validate_icon_dimensions(file):
    from PIL import Image as PILImage
    file.open()
    image = PILImage.open(file)
    width, height = image.size
    if width > 300 or height > 300:
        raise ValidationError("Icon dimensions must not exceed 64x64 pixels.")