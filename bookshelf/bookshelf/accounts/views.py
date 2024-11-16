from django.contrib.auth import authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.contrib import messages

from bookshelf.accounts.forms import LoginForm, CustomerRegistrationForm, CustomerDetailsForm
from bookshelf.accounts.models import CustomerModel


# Create your views here.


class CustomerLoginView(LoginView):
    template_name = 'accounts/login.html'
    form_class = LoginForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            return super().post(request, *args, **kwargs)
        else:
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is None:
                messages.error(request, 'Invalid username or password.')

            return self.form_invalid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class CustomerLogoutView(LogoutView, LoginRequiredMixin):
    template_name = 'accounts/logout.html'


def logout(request):
    return render(request, 'accounts/logout.html')


class CustomerRegistrationView(CreateView):
    form_class = CustomerRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login')


class CustomerDetailsView(DetailView):
    model = CustomerModel
    template_name = 'accounts/account_details.html'
    pk_url_kwarg = 'id'
    context_object_name = 'customer'


class EditAccountView(LoginRequiredMixin, UpdateView):
    template_name = 'accounts/edit_account.html'
    pk_url_kwarg = 'id'
    model = CustomerModel
    form_class = CustomerDetailsForm

    def get_success_url(self):
        customer_id = self.object.id
        print(customer_id)
        return reverse_lazy('account-details', kwargs={'id': customer_id})


class DeleteAccountView(DeleteView):
    template_name = 'accounts/delete_account.html'
    pk_url_kwarg = 'id'
    model = CustomerModel
    success_url = reverse_lazy('home')