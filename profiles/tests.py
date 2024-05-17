from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import Profile
from .serializers import ProfileSerializer


class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="12345"
        )

    def test_profile_creation(self):
        self.assertTrue(Profile.objects.filter(owner=self.user).exists())

    def test_profile_string_representation(self):
        profile = Profile.objects.get(owner=self.user)
        self.assertEqual(str(profile), f"{self.user.username}'s profile")


class ProfileSerializerTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="testuser", password="12345"
        )
        self.profile = Profile.objects.get(owner=self.user)

    def test_serializer_with_valid_data(self):
        request = self.factory.get("/profiles/")
        request.user = self.user
        serializer_context = {
            "request": request,
        }
        serializer = ProfileSerializer(
            instance=self.profile, context=serializer_context
        )
        data = serializer.data

        self.assertEqual(data["owner"], self.user.username)


class ProfileListViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="12345"
        )
        self.url = reverse("profile-list")

    def test_list_profiles(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        paginated_data = response.data.get("results", [])
        total_profiles = Profile.objects.count()

        expected_count = min(10, total_profiles)
        self.assertEqual(len(paginated_data), expected_count)

        self.assertEqual(response.data.get("count"), total_profiles)


class ProfileDetailViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="12345"
        )
        self.profile = Profile.objects.get(owner=self.user)
        self.url = reverse("profile-detail", kwargs={"pk": self.profile.id})

    def test_retrieve_profile(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["owner"], self.user.username)

    def test_update_profile(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.url, {"name": "New Name"})
        self.profile.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.profile.name, "New Name")
