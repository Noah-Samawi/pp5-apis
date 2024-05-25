from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from likes.models import Like
from posts.models import Post
from comments.models import Comment


class LikeTests(TestCase):
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
        self.comment = Comment.objects.create(
            owner=self.user1, post=self.post, content="Comment Content"
        )
        self.client = APIClient()

    def test_like_creation(self):
        self.client.login(username="user1", password="password123")
        response = self.client.post("/likes/", {"post": self.post.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Like.objects.count(), 1)

    def test_like_list_retrieval(self):
        Like.objects.create(owner=self.user1, post=self.post)
        self.client.login(username="user1", password="password123")
        response = self.client.get("/likes/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        like_data = response.data.get("results", response.data)
        self.assertEqual(len(like_data), 1)
        self.assertEqual(like_data[0]['post'], self.post.id)

    def test_like_deletion(self):
        like = Like.objects.create(owner=self.user1, post=self.post)
        self.client.login(username="user1", password="password123")
        response = self.client.delete(f"/likes/{like.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Like.objects.count(), 0)

    def test_prevent_duplicate_likes(self):
        Like.objects.create(owner=self.user1, post=self.post)
        self.client.login(username="user1", password="password123")
        response = self.client.post("/likes/", {"post": self.post.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Like.objects.count(), 1)

    def test_like_creation_for_comment(self):
        self.client.login(username="user1", password="password123")
        response = self.client.post("/likes/", {"comment": self.comment.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Like.objects.count(), 1)

    def test_prevent_duplicate_likes_for_comment(self):
        Like.objects.create(owner=self.user1, comment=self.comment)
        self.client.login(username="user1", password="password123")
        response = self.client.post("/likes/", {"comment": self.comment.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Like.objects.count(), 1)
