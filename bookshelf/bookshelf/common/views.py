from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.functions import Concat
from django.http import JsonResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, DetailView, ListView, CreateView, UpdateView, DeleteView
from bookshelf.book.forms import UpdateCommentForm, DeleteCommentForm
from bookshelf.book.models import Book, Rating, Comment
from django.contrib import messages
from django.db.models import Q, F, Value, CharField
import random
from .forms import CreateReportForm
from .models import Report, QuizResults
from ..author.models import Author
from ..mixins import PermissionCheckMixin, MinUniqueAuthors, MinBooksNeeded
import json


# Create your views here.

class FrontPageView(TemplateView):
    template_name = 'common/front_page.html'


class HomePageView(ListView):
    template_name = 'common/home.html'
    model = Book
    context_object_name = 'books'


class AddCommentView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        book_id = kwargs.get("book_id")
        book = get_object_or_404(Book, id=book_id)
        text = request.POST.get("text")

        if text:
            Comment.objects.create(user=request.user, book=book, text=text)

        return redirect(reverse_lazy('home'))


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

        while len(all_answers) < 3:
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