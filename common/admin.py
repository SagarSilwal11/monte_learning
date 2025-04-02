from django.contrib import admin
from common.models import ImageContent,Image,Icon
# Register your models here.


@admin.register(Image)
class ImageModelAdmin(admin.ModelAdmin):
    list_display=['id','image','uploaded_at']


@admin.register(ImageContent)
class ImageContentaModelAdmin(admin.ModelAdmin):
    list_display=["id","content_type","object_id","content_object","image"]


@admin.register(Icon)
class IconModelAdmin(admin.ModelAdmin):
    list_display=['id','name','icon_file']