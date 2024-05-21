from rest_framework import serializers
from .models import Wanderer
from followers.models import Follower


class WandererSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    following_id = serializers.SerializerMethodField()
    posts_count = serializers.ReadOnlyField()
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()

    def get_is_owner(self, obj):
        # Method to check if the authenticated user is the owner
        request = self.context['request']
        return request.user == obj.owner

    def get_following_id(self, obj):
        # Method to get the ID of the 'Follower' relationship of
        # the authenticated user and the owner of Wanderer if it exists
        user = self.context['request'].user
        if user.is_authenticated:
            following = Follower.objects.filter(
                owner=user, followed=obj.owner
            ).first()
            return following.id if following else None
        return None

    class Meta:
        model = Wanderer
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'name',
            'content', 'image', 'is_owner', 'following_id',
            'posts_count', 'followers_count', 'following_count',
            'one_important_thing', 'favorite_place'
        ]
