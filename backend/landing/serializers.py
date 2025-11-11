from rest_framework import serializers

class MobileSerializer(serializers.Serializer):
    mobile = serializers.CharField()

    def validate_mobile(self, value):
        if not value.isdigit() or len(value) < 10:
            raise serializers.ValidationError("Invalid mobile")
        return value
