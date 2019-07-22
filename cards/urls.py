from django.urls import path

from . import views

app_name = 'cards'

urlpatterns = [
    path('', views.decks, name='decks'),
    path('<int:deck_id>/', views.detail, name='detail'),
    #path('card/<int:card_id>/', views.display, name='display')
    #path('<int:deck_id>/card', views.display, name='display')
    path('<int:deck_id>/card/<int:card_id>/', views.display, name='display')
]
