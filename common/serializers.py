from django.contrib.auth.models import User,Permission,Group
from rest_framework import serializers

class AssignPermissionSerializer(serializers.Serializer):
    username=serializers.CharField()
    permission_codename=serializers.CharField()
    

    def validate(self,data):
        try:
            data['user']=User.objects.get(username=data['username'])
            data['permission']=Permission.objects.get(codename=data['permission_codename'])
        
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found")
        except Permission.DoesNotExist:
            raise serializers.ValidationError("Invalid Permission codename.")
        return data
    
    def create(self,validated_data):
        user=validated_data['user']
        permission=validated_data['permission']
        user.user_permissions.add(permission)
        return user
    


class AssignGroupSerializer(serializers.Serializer):
    username=serializers.CharField()
    group_name=serializers.CharField()

    def validate(self,data):
        try:
            data['user']=User.objects.get(username=data['username'])
            data['group']=Group.objects.get(name=data['group_name'])
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found")
        except Group.DoesNotExist:
            raise serializers.ValidationError("Group not found.")
        return data
    
    def create(self,validate_data):
        user=validate_data['user']
        group=validate_data['group']
        user.groups.add(group)
        return user 