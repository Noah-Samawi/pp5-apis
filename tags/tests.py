from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import Tag
from .serializers import TagSerializer


class TagSerializerTestCase(TestCase):
    """
    TestCase for testing the TagSerializer.
    """

    def test_serializer_with_valid_data(self):
        """
        Test that the serializer can serialize Tag instances with valid data.
        """
        tag_data = {"name": "Test Tag"}
        serializer = TagSerializer(data=tag_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["name"], "Test Tag")

    def test_serializer_with_empty_data(self):
        """
        Test that the serializer is not valid when 'name' is missing.
        """
        serializer = TagSerializer(data={})
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)


class TagListViewTestCase(TestCase):
    """
    TestCase for testing the TagList view.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up data for the entire TestCase.
        """
        cls.predefined_tag_names = [
            "Technology",
            "Travel",
            "Food",
            "Fashion",
            "Art",
            "Science",
            "Health",
            "Music",
            "Sports",
            "Nature",
            "Business",
            "Education",
            "Photography",
            "History",
            "Literature",
            "Movies",
            "Gaming",
            "Cooking",
            "Fitness",
        ]
        # Assuming these tags are already created in the database
        cls.predefined_tags = [
            Tag.objects.get(name=tag_name)
            for tag_name in cls.predefined_tag_names
        ]

    def setUp(self):
        """
        Set up data for each individual test.
        """
        self.client = APIClient()
        self.url = reverse("tag-list")  # URL for the TagList view

    def test_list_tags(self):
        """
        Test that the API returns a list of predefined tags.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Adjusting for pagination in the response
        returned_tags = response.data.get("results", [])
        # Expecting 10 tags on the first page
        self.assertEqual(len(returned_tags), 10)

        # Optionally, testing the total count of tags
        self.assertEqual(response.data.get("count"), len(self.predefined_tags))

    def test_create_tag(self):
        """
        Test creating a new tag using POST request (expecting 403 forbidden).
        """
        data = {"name": "New Tag"}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
