from django.contrib.auth.models import User
from django.test import TestCase
from django.db import IntegrityError, transaction
from rest_framework import status
from rest_framework.test import APIClient

from countryside.models import Countryside
from posts.models import Post


class CountrysideTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="user1", password="password123"
        )
        self.user2 = User.objects.create_user(
            username="user2", password="password123"
        )
        self.post = Post.objects.create(
            owner=self.user1, content="Post Content"
        )
        self.client = APIClient()

    def test_countryside_creation(self):
        self.client.login(username="user1", password="password123")
        response = self.client.post("/countryside/", {"post": self.post.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Countryside.objects.count(), 1)

    def test_countryside_list_retrieval(self):
        Countryside.objects.create(owner=self.user1, post=self.post)
        self.client.login(username="user1", password="password123")
        response = self.client.get("/countryside/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        countryside_data = response.data.get("results", response.data)
        self.assertEqual(len(countryside_data), 1)
        self.assertEqual(countryside_data[0]['post'], self.post.id)

    def test_countryside_deletion(self):
        countryside = Countryside.objects.create(owner=self.user1, post=self.post)
        self.client.login(username="user1", password="password123")
        response = self.client.delete(f"/countryside/{countryside.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Countryside.objects.count(), 0)

    def test_prevent_duplicate_countryside(self):
        Countryside.objects.create(owner=self.user1, post=self.post)
        self.client.login(username="user1", password="password123")
        try:
            with transaction.atomic():
                response = self.client.post("/countryside/", {"post": self.post.id})
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            pass
        self.assertEqual(Countryside.objects.count(), 1)
