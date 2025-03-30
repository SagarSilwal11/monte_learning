from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinLengthValidator
from django.core.validators import RegexValidator
from contact.validators import validate_name,validate_message
# Create your models here.
class ContactModel(models.Model):
    name=models.CharField(max_length=200,validators=[MinLengthValidator(2),RegexValidator(
        regex=r'^[a-zA-z\s]*$',
        message='Name must contan only letter and spaces '
    )])
    email=models.EmailField(max_length=200,unique=True)
    phone=PhoneNumberField()
    message=models.TextField(max_length=500)
    
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    is_active=models.BooleanField(default=True)
    is_read=models.BooleanField(default=False)
    is_important=models.BooleanField(default=False)
    
