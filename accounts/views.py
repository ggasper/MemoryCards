from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


# Create your views here.
class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'


# Edit user information
def change_user_data(request):
    if request.method == 'POST':
        # Form for changing the password
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
    form = PasswordChangeForm(request.user)
            
    context = {
        'password_form': form
    }
            
    return render(request, 'accounts/change.html', context)
