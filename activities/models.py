from django.db import models
from common.models import BaseContent
# Create your models here.
class ActivitiesModel(BaseContent):
    keywords=models.CharField(max_length=200,default='')
    description=models.CharField(max_length=200,default='')
    slug=models.SlugField(unique=True,default='')
    