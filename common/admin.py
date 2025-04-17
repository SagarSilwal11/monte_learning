from django.contrib import admin
from common.models import Image,ImageContent
# Register your models here.
@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
        list_display=['media_type','file','name','mime_type','size','custom_path','original_file_path','alt_text','caption','source','uploaded_at']
    
@admin.register(ImageContent)
class ImageContentModel(admin.ModelAdmin):
    list_display=['content_type','object_id','image','relation_type']