from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from comments.models import Comment
from posts.models import Post


class CommentTests(TestCase):
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

    def test_comment_creation(self):
        # Testing the ability for a user to comment on a post
        self.client.login(username="user1", password="password123")
        response = self.client.post(
            "/comments/", {"post": self.post.id, "content": "Nice post!"}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)

    def test_comment_list_retrieval(self):
        # Testing the retrieval of a list of comments for a post
        Comment.objects.create(
            owner=self.user1, post=self.post, content="Nice post!"
        )
        self.client.login(username="user1", password="password123")
        response = self.client.get("/comments/", {"post": self.post.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Adjusting for potential pagination in the response
        comment_data = response.data.get("results", response.data)
        self.assertEqual(len(comment_data), 1)

    def test_comment_update(self):
        # Testing that a user can update their comment
        comment = Comment.objects.create(
            owner=self.user1, post=self.post, content="Nice post!"
        )
        self.client.login(username="user1", password="password123")
        response = self.client.patch(
            f"/comments/{comment.id}/", {"content": "Updated content"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verifying that the comment's content has been updated
        comment.refresh_from_db()
        self.assertEqual(comment.content, "Updated content")

    def test_comment_deletion(self):
        # Testing that a user can delete their comment
        comment = Comment.objects.create(
            owner=self.user1, post=self.post, content="Nice post!"
        )
        self.client.login(username="user1", password="password123")
        response = self.client.delete(f"/comments/{comment.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 0)
