import re
from rest_framework import serializers


class MobileSerializer(serializers.Serializer):
    """
    Serializer for mobile number validation.
    Supports Persian mobile numbers with formats: 09123456789, +989123456789, 989123456789
    """
    mobile = serializers.CharField(max_length=20, trim_whitespace=True)

    def validate_mobile(self, value):
        """
        Validate mobile number format.
        Accepts: 09xxxxxxxxx, +989xxxxxxxxx, 989xxxxxxxxx
        """
        # Remove spaces and dashes
        mobile = re.sub(r'[\s\-]', '', value)
        
        # Remove country code prefix if exists
        if mobile.startswith('+98'):
            mobile = '0' + mobile[3:]
        elif mobile.startswith('98'):
            mobile = '0' + mobile[2:]
        
        # Validate format: should start with 09 and be 11 digits
        if not re.match(r'^09\d{9}$', mobile):
            raise serializers.ValidationError(
                "Invalid mobile number format. Use format: 09123456789"
            )
        
        return mobile
