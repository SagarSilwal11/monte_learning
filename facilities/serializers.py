from rest_framework import serializers
from facilities.models import Facilities
from common.models import Image, ImageContent
from django.contrib.contenttypes.models import ContentType
from rest_framework.exceptions import ValidationError

class FacilitySerializers(serializers.ModelSerializer):
    icon_id = serializers.IntegerField(write_only=True, required=False)  # Input field for icon ID
    icon_data = serializers.SerializerMethodField()  # Output field for icon data

    class Meta:
        model = Facilities
        fields = [
            'id',
            'heading',
            'content',
            'created_at',
            'updated_at',
            'is_featured',
            'status',
            'icon_id',
            'icon_data',
        ]

    def get_icon_data(self, obj):
        # Fetch the related icon using the relation_type 'icon'
        icon_link = obj.media_items.filter(relation_type='icon').first()
        if icon_link:
            icon = icon_link.image
            request = self.context.get('request')  # Get the request object from the serializer context
            absolute_url = request.build_absolute_uri(icon.file.url) if request else icon.file.url
            return {
                "id": icon.id,
                "name": icon.name,
                "url":absolute_url,
                "alt_text": icon.alt_text,
                "caption": icon.caption,
                "source": icon.source,
                "mime_type": icon.mime_type,
                "size": icon.size,
            }
        return None

    def validate_icon_id(self, value):
        # Validate that the provided icon ID exists in the Image model
        if value and not Image.objects.filter(id=value, media_type='icon').exists():
            raise ValidationError(f"Icon with ID {value} doesn't exist or is not of type 'icon'.")
        return value

    def create(self, validated_data):
        icon_id = validated_data.pop('icon_id', None)
        facility = Facilities.objects.create(**validated_data)

        if icon_id:
            content_type = ContentType.objects.get_for_model(facility)
            ImageContent.objects.create(
                content_type=content_type,
                object_id=facility.id,
                image_id=icon_id,
                relation_type='icon'
            )
        return facility

    def update(self, instance, validated_data):
        icon_id = validated_data.pop('icon_id', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if icon_id:
            content_type = ContentType.objects.get_for_model(instance)
            # Remove old icon and set new one
            instance.media_items.filter(relation_type='icon').delete()
            ImageContent.objects.create(
                content_type=content_type,
                object_id=instance.id,
                image_id=icon_id,
                relation_type='icon'
            )

        return instance