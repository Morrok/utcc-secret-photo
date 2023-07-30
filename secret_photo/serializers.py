from rest_framework import serializers


class CustomUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    number_of_click = serializers.IntegerField(min_value=4, max_value=10)
    image_data = serializers.FileField()

    def validate_number_of_click(self, value):
        allowed_values = [4, 6, 8, 10]
        if value not in allowed_values:
            raise serializers.ValidationError(
                "Invalid value, allowed values are 4, 6, 8, and 10.")
        return value


class PhotoGallerySerializer(serializers.Serializer):
    photo_name = serializers.CharField()
    description = serializers.CharField(required=False, allow_blank=True)
    image_data = serializers.FileField()
    is_favorite = serializers.BooleanField(required=False)


def validations(request_data):
    return
