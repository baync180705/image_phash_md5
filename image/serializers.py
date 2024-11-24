from rest_framework import serializers
from .models import Image

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'link', 'md5_hash', 'p_hash', 'created_at']
        read_only_fields = ["created_at"]