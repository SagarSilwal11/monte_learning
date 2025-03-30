from django.db import models
from common.models import BaseContent
# Create your models here.
class AboutModel(BaseContent):
    image=None
    image1=models.ImageField(upload_to='images/')
    image2=models.ImageField(upload_to='images/')
    image3=models.ImageField(upload_to='images/')