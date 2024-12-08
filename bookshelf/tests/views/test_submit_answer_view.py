from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from bookshelf.book.models import Book, Author
from bookshelf.common.models import QuizResults


class QuizViewsTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        self.author = Author.objects.create(first_name='John', last_name='Doe', date_of_birth='1980-02-02', user=self.user)
        self.book = Book.objects.create(
            user=self.user,
            author=self.author,
            picture_url="http://example.com",
            description="Test description",
            title="Test Book",
        )

        self.submit_answer_url = reverse('submit-answer')
        self.next_question_url = reverse('next-question')

    def test_submit_correct_answer(self):
        data = {
            'user_answer': 'John Doe',
            'book_id': self.book.id
        }
        response = self.client.post(self.submit_answer_url, data, content_type="application/json")

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {'correct': True, 'new_score': 1})

    def test_submit_incorrect_answer(self):
        data = {
            'user_answer': 'Jane Doe',
            'book_id': self.book.id
        }
        response = self.client.post(self.submit_answer_url, data, content_type="application/json")

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {'correct': False})

    def test_submit_creates_quiz_results_if_not_exist(self):
        data = {
            'user_answer': 'John Doe',
            'book_id': self.book.id
        }
        response = self.client.post(self.submit_answer_url, data, content_type="application/json")

        quiz_result = QuizResults.objects.get(user=self.user)
        self.assertEqual(quiz_result.points, 1)

    def test_next_question_returns_valid_data(self):
        response = self.client.get(self.next_question_url)

        self.assertEqual(response.status_code, 200)

        json_response = response.json()
        self.assertIn('question', json_response)
        self.assertIn('answers', json_response)
        self.assertIn('book_id', json_response)