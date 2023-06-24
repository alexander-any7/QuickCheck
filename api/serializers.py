import random
import time
from rest_framework import serializers
from rest_framework.validators import ValidationError

from webapp.models import HackerNewsPost, TYPES


class PostSerializer(serializers.ModelSerializer):
    post_id = serializers.CharField(read_only=True)
    by = serializers.CharField(read_only=True)
    time = serializers.CharField(read_only=True)
    title = serializers.CharField(required=True)
    text = serializers.CharField(required=True)
    type = serializers.CharField()
    url = serializers.CharField()
    source = serializers.CharField(read_only=True)

    class Meta:
        model = HackerNewsPost
        fields = ['id', 'post_id', 'by', 'time', 'title', 'text', 'type', 'url', 'source']

    def validate(self, attrs):
        # Custom validation for the serializer fields
        if self.instance is None:
            # If creating a new instance, validate the 'type' field
            if 'type' not in attrs:
                raise ValidationError('type field is required')
            if attrs['type'] not in TYPES:
                raise ValidationError(f'type can only be one of these choices: {TYPES}')
        else:
            # If updating an existing instance, validate the 'type' field only if present
            if 'type' in attrs and attrs['type'] not in TYPES:
                raise ValidationError(f'type can only be one of these choices: {TYPES}')
        return super().validate(attrs)
    
    def create(self, validated_data):
        # Create a new HackerNewsPost instance
        request = self.context.get('request')
        user = request.user

        # Create the post with validated data
        post = super().create(validated_data)

        # Generate unique values for post_id and time
        post.post_id = random.randint(10_000_000, 99_999_999)
        post.time = int(time.time())

        # Set additional fields
        post.source = 'QuickCheck API'
        post.by = user.username
        post.user_id = user.id
        
        # Save and return the post
        post.save()
        return post