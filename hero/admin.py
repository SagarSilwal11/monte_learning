from django.contrib import admin
from hero.models import Hero
from django.db.models import Q
# Register your models here.

admin.site.site_header="Custom Admin"
@admin.register(Hero)
class HeroModeladmin(admin.ModelAdmin):
    list_display=["id",'heading','content','created_at','updated_at','is_featured','status']
    list_filter=['is_featured','status']

  
    def get_search_results(self, request, queryset, search_term):

        search_terms = [term.strip() for term in search_term.split(',')]
        ids = []

        # Check each term to see if it's a digit and add it to the IDs list
        for term in search_terms:
            if term.isdigit():
                ids.append(int(term))

        # If we have valid IDs, filter the queryset
        if ids:
            queryset = queryset.filter(id__in=ids)

        return queryset, False  # Return the filtered queryset and indicate no further search
    
    def get_status_display(self, obj):
        """Return the display value of the status field."""
        return "In Progress" if obj.status else "Not In Progress"  # Customize this as needed

    get_status_display.short_description = 'Progress'  # This will be the column header in the admin panel