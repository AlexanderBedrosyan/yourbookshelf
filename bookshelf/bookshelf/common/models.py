from django.db import models
from django.http import JsonResponse
from django.views import View

from .choices import LevelChoices
from bookshelf.accounts.models import CustomerModel


# Create your models here.


class Report(models.Model):
    title = models.CharField(
        max_length=100
    )
    user = models.ForeignKey(
        to=CustomerModel,
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )
    report_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class QuizResults(models.Model):
    user = models.OneToOneField(
        to=CustomerModel,
        on_delete=models.CASCADE,
        related_name='quiz_results'
    )

    points = models.PositiveIntegerField(
        default=0
    )

    level = models.CharField(
        max_length=50,
        choices=LevelChoices.choices,
        editable=False
    )

    def save(self, *args, **kwargs):
        if self.points < 100:
            self.level = LevelChoices.AMATEUR
        elif 100 <= self.points <= 199:
            self.level = LevelChoices.SEMI_PRO
        elif 200 <= self.points <= 399:
            self.level = LevelChoices.PRO
        elif 400 <= self.points <= 999:
            self.level = LevelChoices.WORLD_CLASS
        else:
            self.level = LevelChoices.KING

        super().save(*args, **kwargs)


class SubmitAnswerView(View):
    def post(self, request, *args, **kwargs):
        import json
        data = json.loads(request.body)

        user_answer = data.get('user_answer')
        correct_answer = data.get('correct_answer')

        user = request.user

        try:
            quiz_result = QuizResults.objects.get(user=user)
        except QuizResults.DoesNotExist:
            quiz_result = QuizResults(user=user, points=0)

        if user_answer == correct_answer:
            quiz_result.points += 1
            quiz_result.save()
            return JsonResponse({'correct': True, 'new_score': quiz_result.points})
        else:
            return JsonResponse({'correct': False})
