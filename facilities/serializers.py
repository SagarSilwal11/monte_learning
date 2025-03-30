from facilities.models import Facilities
from rest_framework import serializers

class FacilitySerializer(serializers.ModelSerializer):
    # icon=serializers.SerializerMethodField()#convert path to full url automaticaally
    # def get_icon(self,obj):
    #     request=self.context.get("request")#ensure the request exists
    #     if obj.icon and request:
    #         return request.build_absolute_uri(obj.icon.url)
    #     return None  # return None if no
    icon=serializers.ImageField(use_url=True)
    class Meta:
        model=Facilities
        fields="__all__"