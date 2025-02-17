from django.test import TestCase
from django.contrib.auth.models import User
from app.tests.generator import AccountsFactory

class UserTestCase(TestCase):
    def setUp(self):
        self.user = AccountsFactory()  # Creates a single user
        self.users = AccountsFactory.create_batch(10)  # Creates 10 additional users

    def test_user_creation(self):
        self.assertEqual(User.objects.all().count(), 11)  # 1 user + 10 batch users
        self.assertTrue(self.user.check_password("password123"))  # Ensure password is hashed
        