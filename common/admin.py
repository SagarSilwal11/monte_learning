from django.contrib import admin
from common.models import ImageContent
# Register your models here.



@admin.register(ImageContent)
class ImageContentaModelAdmin(admin.ModelAdmin):
    list_display=["id","content_type","object_id","content_object","url"]