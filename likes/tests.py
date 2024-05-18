from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from likes.models import Like
from posts.models import Post


class LikeTests(TestCase):
    def setUp(self):
        # Setting up two users and a post for testing purposes
        self.user1 = User.objects.create_user(
            username="user1", password="password123"
        )
        self.user2 = User.objects.create_user(
            username="user2", password="password123"
        )
        self.post = Post.objects.create(
            owner=self.user1, content="Post Content"
        )

        # Initializing the API client
        self.client = APIClient()

    def test_like_creation(self):
        # Testing the ability for a user to like a post
        self.client.login(username="user1", password="password123")
        response = self.client.post("/likes/", {"post": self.post.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Like.objects.count(), 1)

    def test_like_list_retrieval(self):
        # Testing the retrieval of a list of likes for a user
        Like.objects.create(owner=self.user1, post=self.post)
        self.client.login(username="user1", password="password123")
        response = self.client.get("/likes/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Adjusting for potential pagination in the response
        like_data = response.data.get("results", response.data)
        self.assertEqual(len(like_data), 1)

    def test_like_deletion(self):
        # Testing that a user can delete their like
        like = Like.objects.create(owner=self.user1, post=self.post)
        self.client.login(username="user1", password="password123")
        response = self.client.delete(f"/likes/{like.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Like.objects.count(), 0)

    def test_prevent_duplicate_likes(self):
        # Testing that the system prevents a user
        # from liking a post more than once
        Like.objects.create(owner=self.user1, post=self.post)
        self.client.login(username="user1", password="password123")
        response = self.client.post("/likes/", {"post": self.post.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
