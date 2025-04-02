from django.db import models
from common.models import BaseContent,Icon
# Create your models here.
class Facilities(BaseContent):
    icon=models.ForeignKey(Icon,on_delete=models.SET_NULL,blank=True,null=True)
    

    def __str__(self):
        return self.heading