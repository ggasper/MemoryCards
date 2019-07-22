from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from .models import Card, Deck

import random

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
"""
# Display a card
def display(request, card_id):
    card = get_object_or_404(Card, pk=card_id)

    # Select the next card to show (random)
    deck = get_object_or_404(Deck, pk=card.deck_id)
    next_card_id = random.choice(deck.card_set.all()).pk
    
    return render(request, 'cards/display.html', {'card': card, 'next_id': next_card_id})"""

# Display a random card belonging to deck
def display(request, deck_id, card_id):
    deck = get_object_or_404(Deck, pk=deck_id)
    card = get_object_or_404(Card, pk=card_id)

    # Select card to show
    next_card = random.choice(deck.card_set.all()).pk

    return render(request, 'cards/display.html', {'card': card, 'next_card': next_card})
