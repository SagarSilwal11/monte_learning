from django.db import models
from common.models import BaseContent
# Create your models here.
class Facilities(BaseContent):
    

    def __str__(self):
        return self.heading