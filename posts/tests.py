import json

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from tags.models import Tag

from .models import Post


class PostTests(TestCase):
    def setUp(self):
        # Set up a test user and log in
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client = APIClient()
        self.client.login(username="testuser", password="testpassword")

        # Check if the tag exists, otherwise create it
        try:
            self.tag = Tag.objects.get(name="Technology")
        except Tag.DoesNotExist:
            self.tag = Tag.objects.create(name="Technology")

        # Manually create a post and associate it with the test tag
        self.post = Post.objects.create(
            owner=self.user, title="Test Post", content="Test Content", tag=self.tag
        )

    def test_create_post(self):
        # Test retrieving a post and verify it has the correct tag
        response = self.client.get(f"/posts/{self.post.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        post_response_data = json.loads(response.content)
        self.assertEqual(post_response_data.get("tag", ""), "Technology")

    def test_get_post_list(self):
        # Test retrieving the list of posts
        response = self.client.get("/posts/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_post_detail(self):
        # Test retrieving the details of a specific post
        post = Post.objects.create(owner=self.user, title="Test Post")
        response = self.client.get(f"/posts/{post.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_post(self):
        # Test updating a post's title
        post = Post.objects.create(owner=self.user, title="Test Post")
        updated_data = {"title": "Updated Test Post"}
        response = self.client.patch(
            f"/posts/{post.id}/", updated_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_post(self):
        # Test deleting a post
        post = Post.objects.create(owner=self.user, title="Test Post")
        response = self.client.delete(f"/posts/{post.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
