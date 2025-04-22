from django.db import models
from django.core.validators import MinLengthValidator


class BaseContent(models.Model):
    heading = models.CharField(max_length=200,validators=[MinLengthValidator(5)])
    content = models.TextField(validators=[MinLengthValidator(10)])
    image = models.ImageField(upload_to='images/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_featured = models.BooleanField(default=False)
    status = models.BooleanField(default=True,verbose_name='progress')

    class Meta:
        abstract = True 

    def __str__(self):
        return self.heading
    
    def get_fields(self):
        """Exclude fields dynamically if needed."""
        excluded_fields = getattr(self.__class__, "excluded_fields", [])
        return {field.name: field for field in self._meta.fields if field.name not in excluded_fields}

