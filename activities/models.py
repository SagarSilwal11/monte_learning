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
    
        if not self.keywords:
            base_keywords = slugify(self.heading)
            keywords = base_keywords
            counter = 1
            qs = ActivitiesModel.objects.filter(keywords__iexact=keywords)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            while qs.exists():
                keywords = f"{base_keywords}-{counter}"
                counter += 1
                qs = ActivitiesModel.objects.filter(keywords__iexact=keywords)
                if self.pk:
                    qs = qs.exclude(pk=self.pk)
            self.keywords = keywords

    # Unique description (case-insensitive and ignore self)
        if not self.description:
            base_description = f"Image for {self.heading}"
            description = base_description
            counter = 1
            qs = ActivitiesModel.objects.filter(description__iexact=description)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            while qs.exists():
                description = f"{base_description}-{counter}"
                counter += 1
                qs = ActivitiesModel.objects.filter(description__iexact=description)
                if self.pk:
                    qs = qs.exclude(pk=self.pk)
            self.description = description

    # Save object
        super().save(*args, **kwargs)