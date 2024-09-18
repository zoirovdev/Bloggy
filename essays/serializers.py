from rest_framework import serializers
from .models import Essay


class EssaySerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True, required=False)
    created_at = serializers.DateTimeField(format="%d %b %Y", read_only=True)
    updated_at = serializers.DateTimeField(format="%d %b %Y", read_only=True)

    class Meta:
        model = Essay
        fields = ['id', 'title', 'content', 'image', 'author', 'created_at', 'updated_at']
