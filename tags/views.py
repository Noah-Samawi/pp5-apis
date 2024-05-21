from rest_framework import generics, permissions
from pp5_api.permissions import IsOwnerOrReadOnly
from .models import Tags
from .serializers import TagsSerializer


class TagsList(generics.ListCreateAPIView):
    """
    List all tags items. Create an item if authenticated.
    The perform_create method associates the item with the logged in user.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = TagsSerializer
    queryset = Tags.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TagsDetail(generics.RetrieveDestroyAPIView):
    """
    Retrieve an item. No Update view, as users can
    only add or remove a post as a tags item for now.
    Destroy an item, i.e.  remove a post if owner of that item.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = TagsSerializer
    queryset = Tags.objects.all()
