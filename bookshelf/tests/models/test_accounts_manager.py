from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError


class CustomerManagerTests(TestCase):
    def setUp(self):
        self.user_model = get_user_model()

    def test_create_user_with_valid_data(self):
        user = self.user_model.objects.create_user(
            username="testuser",
            password="testpassword123",
        )
        self.assertEqual(user.username, "testuser")
        self.assertTrue(user.check_password("testpassword123"))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser_with_valid_data(self):
        superuser = self.user_model.objects.create_superuser(
            username="superuser",
            password="superpassword123",
        )
        self.assertEqual(superuser.username, "superuser")
        self.assertTrue(superuser.check_password("superpassword123"))
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_create_user_without_username(self):
        with self.assertRaises(ValueError) as context:
            self.user_model.objects.create_user(username=None, password="password123")
        self.assertEqual(str(context.exception), "The given username must be set")

    def test_create_superuser_missing_is_staff(self):
        with self.assertRaises(ValueError) as context:
            self.user_model.objects.create_superuser(
                username="superuser",
                password="password123",
                is_staff=False,
            )
        self.assertEqual(str(context.exception), "Superuser must have is_staff=True.")

    def test_create_superuser_missing_is_superuser(self):
        with self.assertRaises(ValueError) as context:
            self.user_model.objects.create_superuser(
                username="superuser",
                password="password123",
                is_superuser=False,
            )
        self.assertEqual(str(context.exception), "Superuser must have is_superuser=True.")
