from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'


# Edit user information
#def edit_user(request):
