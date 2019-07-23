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
def display(request, deck_id, page_num):
    deck = get_object_or_404(Deck, pk=deck_id)
    cards = deck.card_set.all().order_by('id')

    # Convert decks page number to card id
    def num_to_id(page_num):
        if 0 < page_num < len(cards) + 1:
            return cards[page_num - 1].pk
        else:
            raise Http404

    card_id = num_to_id(page_num)
    card = get_object_or_404(Card, pk=card_id)

    # Select card to show
    next_card = page_num % len(cards) + 1
    next_card_random = random.choice(cards).pk
    prev_card = page_num - 1
    if prev_card <= 0:
        prev_card = len(cards)
    
    return render(request, 'cards/display.html', {'card': card, 'next_card': next_card, 'prev_card': prev_card, 'next_card_random': next_card_random})
