from django.contrib import admin
from common.models import Image,ImageContent
# Register your models here.

@admin.register(Image)
class ImageModelAdmin(admin.ModelAdmin):
    list_display=["id","url","created_at","updated_at"]

@admin.register(ImageContent)
class ImageContentModelAdmin(admin.ModelAdmin):
    list_display=["id","content_type","object_id","content_object","image_id"]