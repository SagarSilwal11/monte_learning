from django.contrib import admin
from testimonials.models import Testimonials
# Register your models here.
@admin.register(Testimonials)
class TestimonialsModel(admin.ModelAdmin):
    list_display=["quote","name", "designation","image" ,"is_active", "created_at"]