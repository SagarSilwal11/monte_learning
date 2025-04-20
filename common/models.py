from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey,GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from datetime import datetime
from common.validators import validate_alt_text,validate_caption,validate_icon_file,validate_icon_size,validate_image_file,validate_image_size,validate_name_length,validation_media,validate_image_dimensions,validate_icon_dimensions
import os

def upload_to_media(instance, filename):
    folder = 'images' if instance.media_type == 'image' else 'icons'
    return  os.path.join(folder,filename)


def custom_path(instance,filename):
    ext=filename.split(".")[-1]
    customfilename=f"{datetime.now().strftime("%Y%m%d_%H%M%S")}.{ext}"
    return f"{instance.media_type}/{datetime.now().strftime("%Y/%m/%d")}/{customfilename}"

class Image(models.Model):
    MEDIA_TYPE_CHOICES = (
        ('image', 'Image'),
        ('icon', 'Icon'),
    )
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES,validators=[validation_media])
    file=models.ImageField(upload_to=upload_to_media,blank=True,null=True)
    name=models.CharField(max_length=255,blank=True,null=True,validators=[validate_name_length])
    # Auto Metadata
    mime_type = models.CharField(max_length=50, blank=True, null=True)
    size = models.PositiveIntegerField(blank=True, null=True,validators=[validate_image_size])
    custom_path = models.CharField(max_length=255, blank=True, null=True)
    original_file_path = models.CharField(max_length=255, blank=True, null=True)
        # Optional Fields (User-input)
    alt_text = models.CharField(max_length=255, blank=True, null=True,validators=[validate_alt_text])
    caption = models.TextField(blank=True, null=True,validators=[validate_caption])
    source = models.CharField(max_length=255, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.file:
            try:
                # Set metadata
                self.original_file_path = self.file.name
                self.mime_type = self.file.file.content_type
                self.size = self.file.size
                self.custom_path = custom_path(self, self.file.name)

                # Set default name and alt text if not provided
                if not self.name:
                    self.name = self.file.name
                if not self.alt_text:
                    self.alt_text = f"Image for {self.file.name}"

                # Apply validations based on media type
                if self.media_type == 'image':
                    validate_image_file(self.file)  # Validate file type for images
                    validate_image_size(self.file.size)  # Validate file size for images
                    validate_image_dimensions(self.file)  # Validate dimensions for images
                elif self.media_type == 'icon':
                    validate_icon_file(self.file)  # Validate file type for icons
                    validate_icon_size(self.file.size)  # Validate file size for icons
                    validate_icon_dimensions(self.file)  # Validate dimensions for icons

                # Save the object if all validations pass
                super().save(*args, **kwargs)

            except ValidationError as e:
                # Raise validation error
                raise ValidationError(f"Validation failed: {e}")
            except Exception as e:
                # Raise unexpected error
                raise ValidationError(f"An unexpected error occurred: {e}")
    def __str__(self):
        return self.name
    
class ImageContent(models.Model):
    content_type=models.ForeignKey(ContentType,on_delete=models.CASCADE)
    object_id=models.PositiveIntegerField()
    content_object=GenericForeignKey("content_type","object_id")
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    relation_type = models.CharField(
        max_length=20,
        choices=(('main_image', 'Main Image'), ('icon', 'Icon')),
        default='main_image'
    )
    def clean(self):
        model_name = self.content_type.model

        # Validation logic based on model name
        if model_name == 'facilities' and self.image.media_type != 'icon':
            raise ValidationError("Facility can only be linked with icons.")
        elif model_name in ['hero', 'activities'] and self.image.media_type != 'image':
            raise ValidationError(f"{model_name.title()} can only be linked with images.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

 
    
class BaseContent(models.Model):
    heading = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)
    status = models.BooleanField(default=True, verbose_name='progress')

    # Link to MediaAssociation (each model can have media associated)
    media_items = GenericRelation(ImageContent)

    class Meta:
        abstract = True

    def __str__(self):
        return self.heading