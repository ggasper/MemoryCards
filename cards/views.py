from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from .models import Card, Deck

# Create your views here.

# list all deck by publication date
def decks(request):
    deck_list = Deck.objects.order_by('-pub_date')
    context = {'deck_list': deck_list}
    return render(request, 'cards/decks.html', context)

# Display the details of a single deck
def detail(request, deck_id):
    deck = get_object_or_404(Deck, pk=deck_id)
    return render(request, 'cards/detail.html', {'deck': deck})
