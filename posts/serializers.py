from rest_framework import serializers
from posts.models import Post
from likes.models import Like
from countryside.models import Countryside
from django.contrib.humanize.templatetags.humanize import naturaltime


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    wanderer_id = serializers.ReadOnlyField(source='owner.wanderer.id')
    wanderer_image = serializers.ReadOnlyField(source='owner.wanderer.image.url')
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    like_id = serializers.SerializerMethodField()
    likes_count = serializers.ReadOnlyField()
    countryside_id = serializers.SerializerMethodField()
    comments_count = serializers.ReadOnlyField()

    # Convert creation and update time to human-readable format
    def get_created_at(self, obj):
        return naturaltime(obj.created_at)

    def get_updated_at(self, obj):
        return naturaltime(obj.updated_at)

    # Validate image size and dimensions
    def validate_image(self, value):
        if value.size > 2 * 1024 * 1024:
            raise serializers.ValidationError('Image size larger than 2MB!')
        if value.image.height > 4096:
            raise serializers.ValidationError('Image height larger than 4096px!')
        if value.image.width > 4096:
            raise serializers.ValidationError('Image width larger than 4096px!')
        return value

    # Check if the authenticated user is the owner of the post
    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    # Get like ID associated with the authenticated user and the post
    def get_like_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            like = Like.objects.filter(owner=user, post=obj).first()
            return like.id if like else None
        return None

    # Get countryside ID associated with the authenticated user and the post
    def get_countryside_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            countryside = Countryside.objects.filter(owner=user, post=obj).first()
            return countryside.id if countryside else None
        return None

    class Meta:
        model = Post
        fields = [
            'id', 'owner', 'is_owner', 'wanderer_id', 'wanderer_image',
            'created_at', 'updated_at', 'title', 'content', 'image',
            'likes_count', 'comments_count', 'like_id', 'countryside_id',
            'location', 'country'
        ]
