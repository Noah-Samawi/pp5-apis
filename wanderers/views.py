from django.db.models import Count
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from pp5_api.permissions import IsOwnerOrReadOnly
from .models import Wanderer
from .serializers import WandererSerializer


class WandererList(generics.ListAPIView):
    """
    List all wanderers.
    No create view as wanderer creation is handled by django signals.
    This viewset also handles filtering by fields defined in `filterset_fields`
    and ordering by fields defined in `ordering_fields`.
    """
    queryset = Wanderer.objects.annotate(
        posts_count=Count('owner__post', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True)
    ).order_by('-created_at')
    serializer_class = WandererSerializer
    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = [
        'owner__following__followed__wanderer',
        'owner__followed__owner__wanderer',
    ]
    ordering_fields = [
        'posts_count',
        'followers_count',
        'following_count',
        'owner__following__created_at',
        'owner__followed__created_at',
    ]


class WandererDetail(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update a wanderer if you're the owner.
    This viewset also applies the IsOwnerOrReadOnly permission to ensure
    that only the owner of a wanderer instance can update it.
    """
    permission_classes = [IsOwnerOrReadOnly]

    queryset = Wanderer.objects.annotate(
        posts_count=Count('owner__post', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True)
    ).order_by('-created_at')
    serializer_class = WandererSerializer
