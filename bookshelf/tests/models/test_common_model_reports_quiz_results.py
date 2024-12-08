from django.test import TestCase
from django.contrib.auth import get_user_model
from bookshelf.common.models import Report, QuizResults
from bookshelf.common.choices import LevelChoices


class ReportModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')

    def test_report_creation(self):
        report = Report.objects.create(title='Test Report', user=self.user, report_text='Some text')
        self.assertEqual(str(report), 'Test Report')
        self.assertEqual(report.user, self.user)
        self.assertEqual(report.report_text, 'Some text')


class QuizResultsModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')

    def test_quiz_results_creation(self):
        quiz_result = QuizResults.objects.create(user=self.user, points=50)
        self.assertEqual(quiz_result.level, LevelChoices.AMATEUR)

    def test_quiz_results_level_update(self):
        quiz_result = QuizResults.objects.create(user=self.user, points=150)
        self.assertEqual(quiz_result.level, LevelChoices.SEMI_PRO)

        quiz_result.points = 250
        quiz_result.save()
        self.assertEqual(quiz_result.level, LevelChoices.PRO)

        quiz_result.points = 500
        quiz_result.save()
        self.assertEqual(quiz_result.level, LevelChoices.WORLD_CLASS)

        quiz_result.points = 1000
        quiz_result.save()
        self.assertEqual(quiz_result.level, LevelChoices.KING)
