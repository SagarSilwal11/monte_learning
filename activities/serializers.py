from rest_framework import serializers
from activities.models import ActivitiesModel
from common.models import Image, ImageContent
from django.contrib.contenttypes.models import ContentType
from rest_framework.exceptions import ValidationError

class ActivitiesModelSerializers(serializers.ModelSerializer):
    image_id = serializers.IntegerField(write_only=True, required=False)
    image_data = serializers.SerializerMethodField()

    class Meta:
        model = ActivitiesModel
        fields = ['id',
            'heading',
            'content',
            'created_at',
            'updated_at',
            'is_featured',
            'status',
            'keywords',
            'description',
            'slug',
            'image_id',
            'image_data',
        ]

    def get_image_data(self, obj):
        image_link = obj.media_items.filter(relation_type='main_image').first()
        if image_link:
            image = image_link.image
            return {
                "id": image.id,
                "name": image.name,
                "url": image.file.url,
                "alt_text": image.alt_text,
                "caption": image.caption,
                "source": image.source,
                "mime_type": image.mime_type,
                "size": image.size,
            }
        return None

    def validate_image_id(self, value):
        if value and not Image.objects.filter(id=value).exists():
            raise ValidationError(f"Image with ID {value} doesn't exist.")
        return value

    def validate_content(self, value):
        if len(value) <= 10:
            raise ValidationError("Please provide content longer than 10 characters.")
        if len(value) > 200:
            raise ValidationError("Please provide content shorter than 200 characters.")
        return value

    def create(self, validated_data):
        image_id = validated_data.pop('image_id', None)
        activity = ActivitiesModel.objects.create(**validated_data)

        if image_id:
            content_type = ContentType.objects.get_for_model(activity)
            ImageContent.objects.create(
                content_type=content_type,
                object_id=activity.id,
                image_id=image_id,
                relation_type='main_image'
            )
        return activity

    def update(self, instance, validated_data):
        image_id = validated_data.pop('image_id', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if image_id:
            content_type = ContentType.objects.get_for_model(instance)
            instance.media_items.filter(relation_type='main_image').delete()
            ImageContent.objects.create(
                content_type=content_type,
                object_id=instance.id,
                image_id=image_id,
                relation_type='main_image'
            )

        return instance
