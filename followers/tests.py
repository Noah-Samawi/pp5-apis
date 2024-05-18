from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from followers.models import Follower


class FollowerTests(TestCase):
    def setUp(self):
        # Setting up two users for testing purposes
        self.user1 = User.objects.create_user(
            username="user1", password="password123"
        )
        self.user2 = User.objects.create_user(
            username="user2", password="password123"
        )

        # Initializing the API client
        self.client = APIClient()

    def test_follow_creation(self):
        # Testing the ability for a user to follow another user
        self.client.login(username="user1", password="password123")
        response = self.client.post("/followers/", {"followed": self.user2.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Follower.objects.count(), 1)

    def test_follower_list_retrieval(self):
        # Testing the retrieval of a list of followers for a user
        Follower.objects.create(owner=self.user1, followed=self.user2)
        self.client.login(username="user1", password="password123")
        response = self.client.get("/followers/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Adjusting for potential pagination in the response
        follower_data = response.data.get("results", response.data)
        self.assertEqual(len(follower_data), 1)

    def test_follower_deletion(self):
        # Testing that a user can unfollow another user
        follower = Follower.objects.create(
            owner=self.user1, followed=self.user2
        )
        self.client.login(username="user1", password="password123")
        response = self.client.delete(f"/followers/{follower.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Follower.objects.count(), 0)

    def test_prevent_duplicate_followers(self):
        # Testing that the system prevents a user from
        # following the same user more than once
        Follower.objects.create(owner=self.user1, followed=self.user2)
        self.client.login(username="user1", password="password123")
        response = self.client.post("/followers/", {"followed": self.user2.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
