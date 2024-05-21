from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers


# Custom serializer for user details.
# This serializer extends the UserDetailsSerializer from
# 'dj_rest_auth' to include 'wanderer_id' and 'wanderer_image' fields.
# These additional fields are read-only and sourced from the
# related 'wanderer' object.
class CurrentUserSerializer(UserDetailsSerializer):
    wanderer_id = serializers.ReadOnlyField(source='wanderer.id')
    wanderer_image = serializers.ReadOnlyField(source='wanderer.image.url')

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + (
            'wanderer_id', 'wanderer_image'
        )