from django.contrib import admin
from activities.models import ActivitiesModel
# Register your models here.
@admin.register(ActivitiesModel)
class ActiviteModelAdmin(admin.ModelAdmin):
    list_display=["id",'heading','content','created_at','updated_at','is_featured','status','keywords','description','slug']
    list_filter=['is_featured','status']
    
    def get_status_display(self, obj):
        """Return the display value of the status field."""
        return "In Progress" if obj.status else "Not In Progress"  # Customize this as needed

    get_status_display.short_description = 'Progress'  # This will be the column header in the admin panel