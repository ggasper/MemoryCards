from django.urls import path

from . import views

app_name = 'cards'

urlpatterns = [
    path('', views.decks, name='decks'),
    path('<int:deck_id>/', views.detail, name='detail'),
]
