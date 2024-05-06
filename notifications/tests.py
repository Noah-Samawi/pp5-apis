from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from comments.models import Comment
from followers.models import Follower
from likes.models import Like
from notifications.models import Notification
from posts.models import Post


class NotificationTests(TestCase):
    def setUp(self):
        # Setting up two users for testing
        self.user1 = User.objects.create_user(
            username="user1", password="password123"
        )
        self.user2 = User.objects.create_user(
            username="user2", password="password123"
        )

        # Initializing the API client and logging in with user1
        self.client = APIClient()
        self.client.login(username="user1", password="password123")

        # Creating a test post with user1 as the owner
        self.post = Post.objects.create(
            owner=self.user1, content="Post Content"
        )

    def test_create_comment_notification(self):
        # Creating a comment on the post and checking for the
        # creation of a notification
        comment = Comment.objects.create(
            owner=self.user2, post=self.post, content="Nice post!"
        )
        notification = Notification.objects.filter(
            recipient=self.user1, notification_type="comment"
        ).first()
        self.assertIsNotNone(notification)
        self.assertEqual(notification.related_object_id, self.post.id)

    def test_create_like_notification(self):
        # Creating a like on the post and checking for the
        # creation of a notification
        like = Like.objects.create(owner=self.user2, post=self.post)
        notification = Notification.objects.filter(
            recipient=self.user1, notification_type="like"
        ).first()
        self.assertIsNotNone(notification)
        self.assertEqual(notification.related_object_id, self.post.id)

    def test_create_follower_notification(self):
        # Creating a follower relationship and checking for the
        # creation of a notification
        follower = Follower.objects.create(
            owner=self.user2, followed=self.user1
        )
        notification = Notification.objects.filter(
            recipient=self.user1, notification_type="follower"
        ).first()
        self.assertIsNotNone(notification)
        self.assertEqual(notification.related_object_id, self.user2.id)

    def test_notification_list_retrieval(self):
        # Testing the retrieval of a user's notification list
        response = self.client.get("/notifications/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_notification_update(self):
        # Testing the update functionality of a notification
        # (marking it as read)
        notification = Notification.objects.create(
            recipient=self.user1,
            message="Test",
            notification_type="like",
            related_object_id=1,
        )
        response = self.client.patch(
            f"/notifications/{notification.id}/", {"read": True}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verifying that the notification's read status has been updated
        notification.refresh_from_db()
        self.assertTrue(notification.read)