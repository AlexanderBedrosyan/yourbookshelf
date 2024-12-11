from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.functions import Concat
from django.http import JsonResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, DetailView, ListView, CreateView, UpdateView, DeleteView
from bookshelf.book.forms import UpdateCommentForm, DeleteCommentForm
from bookshelf.book.models import Book, Rating, Comment
from django.contrib import messages
from django.db.models import Q, F, Value, CharField, Avg
import random
from .forms import CreateReportForm, DetailReportForm
from .models import Report, QuizResults
from ..accounts.models import CustomerModel
from ..author.models import Author
from ..mixins import PermissionCheckMixin, MinUniqueAuthors, MinBooksNeeded, PermissionOnlyForStaffs
import json
from django.utils.html import escape



# Create your views here.

class FrontPageView(TemplateView):
    template_name = 'common/front_page.html'


class HomePageView(ListView):
    template_name = 'common/home.html'
    model = Book
    context_object_name = 'books'

    def get_queryset(self):
        return Book.objects.all().order_by('-updated_at', 'title')


class AddCommentView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        book_id = kwargs.get("pk")
        book = get_object_or_404(Book, id=book_id)
        text = request.POST.get("text")

        if text:
            sanitized_text = escape(text)
            comment = Comment.objects.create(user=request.user, book=book, text=sanitized_text)
            return JsonResponse({
                'id': comment.id,
                'text': comment.text,
                'username': comment.user.username,
                'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            })

        return JsonResponse({'error': 'Invalid data'}, status=400)


class AddRatingView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        book_id = kwargs.get("book_id")
        rating_value = request.POST.get("rating")

        if not rating_value or not rating_value.isdigit() or not (1 <= int(rating_value) <= 5):
            return JsonResponse({'error': 'Invalid rating value'}, status=400)

        book = get_object_or_404(Book, id=book_id)

        rating, created = Rating.objects.update_or_create(
            book=book,
            user=request.user,
            defaults={'rating': int(rating_value)}
        )

        new_average_rating = book.ratings.aggregate(Avg('rating'))['rating__avg'] or 0

        return JsonResponse({
            'message': 'Rating added successfully',
            'new_average_rating': round(new_average_rating, 2)
        })


class EditCommentView(LoginRequiredMixin, PermissionCheckMixin, UpdateView):
    template_name = 'book/edit_comment.html'
    pk_url_kwarg = 'pk'
    model = Comment
    form_class = UpdateCommentForm
    success_url = reverse_lazy('home')


class DeleteCommentView(LoginRequiredMixin, PermissionCheckMixin, DeleteView):
    pk_url_kwarg = 'pk'
    template_name = 'book/delete_comment.html'
    success_url = reverse_lazy('home')
    form_class = DeleteCommentForm
    model = Comment

    def get_initial(self):
        return self.object.__dict__

    def form_invalid(self, form):
        return self.form_valid(form)


class PermissionDeniedView(TemplateView):
    template_name = 'common/not_allow_page.html'


class SearchResultsView(ListView):
    template_name = 'common/search.html'
    queryset = Book.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('search-word')
        if query:
            books = Book.objects.filter(Q(title__icontains=query)).distinct()
            authors = Author.objects.filter(
                Q(first_name__icontains=query) | Q(last_name__icontains=query)
            ).distinct()
            context['books'] = books
            context['authors'] = authors
        else:
            context['books'] = Book.objects.none()
            context['authors'] = Author.objects.none()
        return context


class CreateReportView(LoginRequiredMixin, CreateView):
    form_class = CreateReportForm
    template_name = 'common/report.html'
    model = Report
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        if not form.is_valid():
            print(form.errors)
            return self.form_invalid(form)

        form.instance.user = self.request.user
        return super().form_valid(form)


class QuizGameView(LoginRequiredMixin, MinUniqueAuthors, MinBooksNeeded, TemplateView):
    template_name = 'common/quiz.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        books = Book.objects.all()

        random_book = random.choice(books)
        question = f'Кой е автор на книгата "{random_book.title}"?'
        correct_answer = random_book.author
        unique_authors = list(Author.objects.annotate(
                full_name=Concat(
                    F('first_name'),
                    Value(' '),
                    F('last_name'),
                    output_field=CharField()
                )
            ).exclude(full_name=correct_answer).values_list('full_name', flat=True).distinct())
        all_answers = [correct_answer]

        while len(all_answers) < 3:
            wrong_answer = random.choice(unique_authors)

            if wrong_answer not in all_answers:
                all_answers.append(wrong_answer)
                unique_authors.remove(wrong_answer)

        context['question'] = question
        context['answers'] = all_answers
        context['book_id'] = random_book.id

        return context


class SubmitAnswerView(LoginRequiredMixin, MinUniqueAuthors, MinBooksNeeded, View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        user_answer = data.get('user_answer')
        book_id = data.get('book_id')
        book = Book.objects.get(id=book_id)

        user = request.user

        try:
            quiz_result = QuizResults.objects.get(user=user)
        except QuizResults.DoesNotExist:
            quiz_result = QuizResults(user=user, points=0)

        if user_answer == str(book.author.get_full_name()):
            quiz_result.points += 1
            quiz_result.save()
            return JsonResponse({'correct': True, 'new_score': quiz_result.points})
        else:
            return JsonResponse({'correct': False})


class NextQuestionView(View):
    def get(self, request, *args, **kwargs):
        books = Book.objects.all()

        random_book = random.choice(books)
        question = f'Кой е автор на книгата "{random_book.title}"?'
        correct_answer = str(random_book.author)

        unique_authors = list(Author.objects.annotate(
            full_name=Concat(
                F('first_name'),
                Value(' '),
                F('last_name'),
                output_field=CharField()
            )
        ).exclude(full_name=correct_answer).values_list('full_name', flat=True).distinct())

        all_answers = [correct_answer]

        while len(all_answers) < 3 and unique_authors:
            wrong_answer = random.choice(unique_authors)

            if wrong_answer not in all_answers:
                all_answers.append(wrong_answer)
                unique_authors.remove(wrong_answer)

        random.shuffle(all_answers)

        return JsonResponse({
            'question': question,
            'answers': all_answers,
            'book_id': random_book.id
        })


class ReportsView(LoginRequiredMixin, TemplateView):
    template_name = 'common/all_reports.html'

    def has_permission(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def get(self, request, *args, **kwargs):
        if not self.has_permission():
            messages.error(request, "Access denied. You do not have the required permissions to view this page.")
            return redirect('permission-denied')

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reports = Report.objects.all().order_by('created_at')
        context['reports'] = reports
        return context


class SingleReportView(LoginRequiredMixin, PermissionOnlyForStaffs, UpdateView):
    template_name = 'common/single_report.html'
    pk_url_kwarg = 'id'
    form_class = DetailReportForm
    model = Report
    success_url = reverse_lazy('reports')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(instance=self.object)
        return context