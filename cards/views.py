from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.utils import timezone

from .models import Card, Deck
from .forms import DeckForm, DeckEditForm, CardEditForm

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

# Display a card belonging to deck
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
        
    context =  {
        'card': card,
        'next_card': next_card,
        'prev_card': prev_card,
        'next_card_random': next_card_random
    }
    
    return render(request, context, 'cards/display.html',)

# Create a new deck
def create_deck_form(request):
    # if user is not logged in redirect him to the login page
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    if request.method == 'POST':
        form = DeckForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            deck = Deck(title=title, author=request.user, description=description, pub_date=timezone.now())
            deck.save()

            # Allow the user to edit their own decks
            deck.allow_edit(request.user)


        # Create initial card
        card = deck.card_set.create(front="", back="")
        
        # Redirect to deck editing form
        return redirect('cards:edit', card_id = card.pk, deck_id = deck.pk)
    else:
        form = DeckForm()
    return render(request, 'cards/create_deck_form.html', {'form': form})

def edit_deck(request, deck_id, card_id):
    deck = get_object_or_404(Deck, pk=deck_id)
    card = get_object_or_404(Card, pk=card_id)

    if not request.user.has_perm('can_edit', deck):
        return redirect('/')
    
    if request.method == 'POST':
        deck_form = DeckEditForm(request.POST)
        card_form = CardEditForm(request.POST)

        deck.update_from_form(deck_form)
        card.update_from_form(card_form)
        return redirect('/')
    else:
        deck_form = DeckEditForm()
        deck_form.init(deck)
        card_form = CardEditForm()
        card_form.init(card)
        return render(request, 'cards/edit_deck.html', {'deck_form': deck_form, 'card_form': card_form})
    
