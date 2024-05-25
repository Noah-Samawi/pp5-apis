from rest_framework.exceptions import ValidationError
from rest_framework import generics, permissions
from pp5_api.permissions import IsOwnerOrReadOnly
from .models import Like
from .serializers import LikeSerializer


class LikeList(generics.ListCreateAPIView):
    """
    List all likes. Create a like if authenticated.
    The perform_create method associates the like with the logged in user.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = LikeSerializer
    queryset = Like.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        post = serializer.validated_data.get('post')
        comment = serializer.validated_data.get('comment')

        if post and Like.objects.filter(owner=user, post=post).exists():
            raise ValidationError('You have already liked this post.')
        if comment and Like.objects.filter(owner=user, comment=comment).exists():
            raise ValidationError('You have already liked this comment.')

        serializer.save(owner=user)


class LikeDetail(generics.RetrieveDestroyAPIView):
    """
    Retrieve a like. No Update view, as users can
    only like or unlike a post. Destroy a like, i.e.
    unlike a post if owner of that like
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = LikeSerializer
    queryset = Like.objects.all()
