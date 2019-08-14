from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('change/', views.change_user_data, name='change'),
    path('login/', views.login_view, name='login')
]
