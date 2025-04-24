from django.db import models
from common.models import BaseContent
from django.utils.text import slugify
# Create your models here.
class ActivitiesModel(BaseContent):
    keywords=models.CharField(max_length=200,default='')
    description=models.CharField(max_length=200,default='')
    slug=models.SlugField(unique=True,default='')
    
    def save(self, *args, **kwargs):
    # Automatically generate slug from heading if not provided
        if not self.slug:
            self.slug = slugify(self.heading)
    
    # Ensure keywords is unique
        if not self.keywords:
            base_keywords = self.heading
            keywords = base_keywords
            counter = 1
            while ActivitiesModel.objects.filter(keywords=keywords).exists():
                keywords = f"{base_keywords}-{counter}"
                counter += 1
            self.keywords = keywords
    
    # Ensure description is unique
        if not self.description:
            base_description = f"Image for {self.heading}"
            description = base_description
            counter = 1
            while ActivitiesModel.objects.filter(description=description).exists():
                description = f"{base_description}-{counter}"
                counter += 1
            self.description = description
        
        # Save the object to the database
        super().save(*args, **kwargs)