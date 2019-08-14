from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, AuthenticationForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

# Create your views here.
class SignUp(generic.CreateView, SuccessMessageMixin):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'
    success_message = "You have succesfully registered"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['signup'] = True
        return context

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, "Successfully logged in!")
                return redirect('/')
            else:
                messages.errror(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")
    
    form = AuthenticationForm()
    context = {
        'form': form,
        'login': True
    }
    return render(request, 'accounts/login.html', context)

    
# Edit user information
def change_user_data(request):
    if request.method == 'POST':
        # Form for changing the password
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Successfully changed password")
        else:
            messages.error(request, "Failed to change password")
    form = PasswordChangeForm(request.user)
            
    context = {
        'password_form': form,
        'change_account': True
    }
            
    return render(request, 'accounts/change.html', context)
