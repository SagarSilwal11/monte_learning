from django.db import models
from django.core.validators import MaxLengthValidator
# Create your models here.
class Testimonials(models.Model):
    quote=models.TextField(validators=[MaxLengthValidator(150)],help_text="Enter a quote (max 150 characters)")
    name=models.CharField(max_length=100,help_text="Enter the name of the person ")
    designation=models.CharField(max_length=100,blank=True)
    image=models.ImageField(upload_to="testimonials/",unique=True,blank=True,null=True)
    is_active=models.BooleanField(default='True')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'

