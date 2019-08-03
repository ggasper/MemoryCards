from django.urls import path

from . import views

app_name = 'cards'

urlpatterns = [
    path('', views.decks, name='decks'),
    path('<int:deck_id>/', views.detail, name='detail'),
    path('<int:deck_id>/card/<int:page_num>/', views.display, name='display'),
    path('create', views.create_deck_form, name='create'),
    path('edit/<int:deck_id>/<int:card_id>', views.edit_deck, name='edit'),
    path('review/<int:deck_id>', views.review, name='review'),
    path('end_review/<int:deck_id>', views.end_review, name='end_review')
]
