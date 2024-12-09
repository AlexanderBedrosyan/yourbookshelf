from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.contrib.messages.storage.fallback import FallbackStorage
from django.http import HttpResponse
from django.shortcuts import reverse

from bookshelf.author.models import Author
from bookshelf.book.choices import GenreChoices
from bookshelf.mixins import PermissionCheckMixin
from bookshelf.book.models import Book

User = get_user_model()


class TestPermissionCheckMixin(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpass', email='testuser@example.com')
        self.staff_user = User.objects.create_user(
            username='staffuser', password='staffpass', email='staffuser@example.com', is_staff=True
        )
        self.superuser = User.objects.create_superuser(
            username='admin', password='adminpass', email='admin@example.com'
        )
        self.author = Author.objects.create(
            first_name="Jane",
            last_name="Austen",
            date_of_birth="1980-06-02",
            user=self.user,
        )
        self.book = Book.objects.create(
            user=self.user,
            author=self.author,
            picture_url="https://example.com/book.jpg",
            description="This is a valid description.",
            title="Test Book",
            approved=True,
            genre=GenreChoices.FICTION,
        )

    def test_access_allowed_for_authorized_user(self):
        request = self.factory.get(reverse('book-details', kwargs={'id': self.book.id}))

        request.user = User.objects.create_user(username='otheruser', password='pass')
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        class MockView(PermissionCheckMixin):
            def get(self, request, *args, **kwargs):
                return HttpResponse("Success")

        response = MockView().get(request, pk=self.book.id)
        self.assertEqual(response.status_code, 200)

    def test_access_allowed_for_superuser(self):
        request = self.factory.get(reverse('book-details', kwargs={'id': self.book.id}))
        request.user = self.superuser

        class MockView(PermissionCheckMixin):
            def get(self, request, *args, **kwargs):
                return HttpResponse("Success")

        response = MockView().get(request, pk=self.book.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"Success")


