from django.contrib import admin
from contact.models import ContactModel
# Register your models here.
@admin.register(ContactModel)
class ContactModelAdmin(admin.ModelAdmin):
    list_display=['id','name','email','phone','message','created_at','updated_at','is_active','is_read','is_important']