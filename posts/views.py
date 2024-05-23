from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from pp5_api.permissions import IsOwnerOrReadOnly
from .models import Post
from .serializers import PostSerializer
from django.db.models import Count


class PostList(generics.ListCreateAPIView):
    """
    List posts or create a post if logged in
    The perform_create method associates the post with the logged in user.
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Post.objects.annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comment', distinct=True),
        countrysides_count=Count('countryside', distinct=True)
    ).order_by('-created_at')

    # Define filter backends for ordering, searching and filtering
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]

    # Define fields for filtering
    filterset_fields = [
        'owner__followed__owner__wanderer',
        'likes__owner__wanderer',
        'countryside__owner__wanderer',
        'owner__wanderer',
    ]

    # Define fields for searching
    search_fields = [
        'owner__username',
        'title',
        'country',
    ]

    # Define fields for ordering
    ordering_fields = [
        'likes_count',
        'comments_count',
        'countrysides_count',
        'likes__created_at',
        'countrysides__created_at',
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve a post and edit or delete it if you own it.
    """
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]

    queryset = Post.objects.annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comment', distinct=True),
        countrysides_count=Count('countryside', distinct=True)
    ).order_by('-created_at')
