from django.contrib.auth.models import User
from .models import Wanderer
from django.test import TestCase


class UserWandererCountTest(TestCase):
    # make sure that the user is always extended with the wanderer model
    def test_user_wanderer_count(self):
        user_count = User.objects.count()
        wanderer_count = Wanderer.objects.count()
        self.assertEqual(user_count, wanderer_count)
