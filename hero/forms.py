from hero.models import Hero
from django import forms
class HeroForm(forms.ModelForm):
    class Meta:
        model=Hero
        fields="__all__"
        labels={'heading':'Header','content':'content','image':'image',
                'is_featured':'is_featured',
                'is_status':'is_status'}