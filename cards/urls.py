from django.urls import path
from django.http import HttpResponseRedirect

from . import views

app_name = 'cards'

urlpatterns = [
    path('', lambda r: HttpResponseRedirect('1')),
    path('<int:page_num>', views.decks, name='decks'),
    path('my_decks', lambda r: HttpResponseRedirect('my_decks/1')),
    path('my_decks/<int:page_num>', views.my_decks, name='my_decks'),
    path('<int:deck_id>/', views.detail, name='detail'),
    path('<int:deck_id>/card/<int:card_id>/', views.display, name='display'),
    path('create', views.create_deck_form, name='create'),
    path('edit/<int:deck_id>/<int:card_id>', views.edit_deck, name='edit'),
    path('review/<int:deck_id>', views.review, name='review'),
    path('end_review/<int:deck_id>', views.end_review, name='end_review')
]
