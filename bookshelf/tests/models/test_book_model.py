from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from bookshelf.book.models import Book, Rating
from bookshelf.accounts.models import CustomerModel
from bookshelf.author.models import Author
from bookshelf.book.choices import GenreChoices


class BookModelTest(TestCase):
    def setUp(self):
        self.customer = CustomerModel.objects.create(
            username="sakeeE",
            email="john@example.com",
        )
        self.author = Author.objects.create(
            first_name="Jane",
            last_name="Austen",
            date_of_birth="1980-06-02",
            user=self.customer
        )

    def test_create_valid_book(self):
        book = Book.objects.create(
            user=self.customer,
            author=self.author,
            picture_url="https://example.com/book.jpg",
            description="This is a valid description.",
            title="Pride and Prejudice",
            approved=True,
            genre=GenreChoices.FICTION,
        )
        self.assertEqual(book.title, "Pride and Prejudice")
        self.assertEqual(book.genre, GenreChoices.FICTION)
        self.assertTrue(book.approved)

    def test_unique_title(self):
        Book.objects.create(
            user=self.customer,
            author=self.author,
            picture_url="https://example.com/book.jpg",
            description="Description one.",
            title="Unique Title",
            genre=GenreChoices.FICTION,
        )
        with self.assertRaises(IntegrityError):
            Book.objects.create(
                user=self.customer,
                author=self.author,
                picture_url="https://example.com/book2.jpg",
                description="Description two.",
                title="Unique Title",
                genre=GenreChoices.HORROR,
            )

    def test_description_validation(self):
        with self.assertRaises(ValidationError):
            book = Book(
                user=self.customer,
                author=self.author,
                picture_url="https://example.com/book.jpg",
                description="lowercase description that is not valid.",
                title="Invalid Description Test",
                genre=GenreChoices.FICTION,
            )
            book.full_clean()

    def test_average_rating(self):
        book = Book.objects.create(
            user=self.customer,
            author=self.author,
            picture_url="https://example.com/book.jpg",
            description="This is a valid description.",
            title="Test Book",
            genre=GenreChoices.THRILLER,
        )
        self.customer1 = CustomerModel.objects.create(
            username="test",
            email="test@example.com",
        )
        Rating.objects.create(
            book=book,
            user=self.customer,
            rating=5
        )
        Rating.objects.create(
            book=book,
            user=self.customer1,
            rating=3
        )
        self.assertEqual(book.average_rating(), 4)

    def test_default_values(self):
        book = Book.objects.create(
            user=self.customer,
            author=self.author,
            picture_url="https://example.com/book.jpg",
            description="This is a valid description.",
            title="Default Values Test",
        )
        self.assertFalse(book.approved)
        self.assertEqual(book.genre, GenreChoices.OTHERS)

    def test_related_name_books(self):
        book1 = Book.objects.create(
            user=self.customer,
            author=self.author,
            picture_url="https://example.com/book1.jpg",
            description="Description for book 1.",
            title="Book One",
        )
        book2 = Book.objects.create(
            user=self.customer,
            author=self.author,
            picture_url="https://example.com/book2.jpg",
            description="Description for book 2.",
            title="Book Two",
        )
        self.assertEqual(self.customer.books.count(), 2)
        self.assertIn(book1, self.customer.books.all())
        self.assertIn(book2, self.customer.books.all())

