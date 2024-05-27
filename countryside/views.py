from rest_framework import generics, permissions
from pp5_api.permissions import IsOwnerOrReadOnly
from .models import Countryside
from .serializers import CountrysideSerializer


class CountrysideList(generics.ListCreateAPIView):
    """
    List all countryside items. Create an item if authenticated.
    The perform_create method associates the item with the logged in user.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = CountrysideSerializer
    queryset = Countryside.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CountrysideDetail(generics.RetrieveDestroyAPIView):
    """
    Retrieve an item. No Update view, as users can
    only add or remove a post as a countryside item for now.
    Destroy an item, i.e.  remove a post if owner of that item.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = CountrysideSerializer
    queryset = Countryside.objects.all()
