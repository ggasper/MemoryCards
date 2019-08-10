from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .models import Card, Deck, SM2_data
from .forms import DeckForm, DeckEditForm, CardEditForm, RetentionForm
from .sm2 import SM2
from .deck_manager import DeckManager

import random

# Create your views here.

# list all deck by publication date
def decks(request):
    deck_list = Deck.objects.order_by('-pub_date')
    context = {'deck_list': deck_list}
    return render(request, 'cards/decks.html', context)

# List all deck made by user
@login_required
def my_decks(request):
    deck_list = Deck.objects.filter(author=request.user).order_by('-pub_date')
    context = {'deck_list': deck_list}
    return render(request, 'cards/decks.html', context)


# Display the details of a single deck
def detail(request, deck_id):
    deck_manager = DeckManager(deck_id)
    edit_card = deck_manager.get_first_card()
    return render(request, 'cards/detail.html', {'deck': deck_manager.deck, 'edit_card': edit_card, 'can_edit': deck_manager.can_edit(request.user)})

# Display a card belonging to deck
def display(request, deck_id, card_id):
    deck_manager = DeckManager(deck_id)

    if card_id == 0:
        f_card = deck_manager.get_first_card()
        if not f_card:
            return redirect("/")
        else:
            return redirect("cards:display", deck_id, f_card.pk)
    else:
        active_card = get_object_or_404(Card, pk=card_id)
        
    n_card = deck_manager.get_next_card(active_card)
    p_card = deck_manager.get_previous_card(active_card)
    cards_around = deck_manager.get_cards_around(active_card)

    context = {
        'active_card': active_card,
        'n_card': n_card,
        'p_card': p_card,
        'cards_around': cards_around,
        'deck': deck_manager.deck
    }
    
    return render(request, 'cards/display.html', context)

# Create a new deck
@login_required
def create_deck_form(request):
    if request.method == 'POST':
        form = DeckForm(request.POST)
        
        if form.is_valid():
            return DeckManager.new_deck_from_form(request, form)

    form = DeckForm()
    return render(request, 'cards/create_deck_form.html', {'form': form})


# Form for editing the deck
@login_required
def edit_deck(request, deck_id, card_id):

    deck_manager = DeckManager(deck_id)

    if not deck_manager.can_edit(request, user):
        return redirect('/')
    
    # If card_id is 0 then we need to create new card first
    if card_id == 0:
        card = deck_manager.new_blank_card(deck_manager.deck)
        return redirect('cards:edit', deck_id=deck_id, card_id=card.pk)
    else:
        card = get_object_or_404(Card, pk=card_id)
    
    
    if request.method == 'POST':
        deck_form = DeckEditForm(request.POST)
        card_form = CardEditForm(request.POST)

        deck_manager.deck.update_from_form(deck_form)
        card.update_from_form(card_form)
        
    deck_form = DeckEditForm()
    deck_form.init(deck_manager.deck)
    card_form = CardEditForm()
    card_form.init(card)

    # Find next and previous card
    n_card = deck_manager.get_next_card(card)

    # Find pages to display for quick navigation
    cards_around = deck_manager.get_cards_around(card)
    
    context = {
        'deck_form': deck_form,
        'card_form': card_form,
        'deck': deck_manager.deck,
        'n_card': n_card,
        'cards_around': cards_around,
        'active_card': card
    }
        
    p_card = deck_manager.get_previous_card(card)
    if p_card:
        context['p_card'] = p_card
        
    return render(request, 'cards/edit_deck.html', context)

# Display deck for learning with sm2 algorithm
@login_required
def review(request, deck_id):
    sm2 = SM2(request.user, deck_id)

    # Check if we are starting new repeat
    if request.method == 'GET' and 'new' in request.GET and request.GET['new']:
        sm2.start_repeat()
        return redirect('cards:review', deck_id=deck_id)
    
    # If we have some data to update first process that
    if request.method == 'POST':
        
        form = RetentionForm(request.POST)
        print(form.errors)
        if form.is_valid():
            quality = int(form.cleaned_data['quality'][0])
            #print(quality)
            sm2_data_id = int(form.cleaned_data['sm2_data_id'])

            sm2_data = get_object_or_404(SM2_data, pk=sm2_data_id)

            # The repetition counter equals zero if we got here from inital repetition and something else if we are just repeating bad
            # attempts.
            if sm2_data.needs_review():
                sm2.update_card(sm2_data.card, quality)
            else:
                sm2.update_card_bq(sm2_data.card, quality)
    # Get new card if there is one
    sm2_card = sm2.get_card()

    # If there is no card that hasn't been reviewed yet, choose one from the poorly graded ones
    if not sm2_card:
        sm2_card = sm2.get_card_bq()
    # If there is still no card, we are done
    if not sm2_card:
        return redirect('cards:end_review', deck_id=deck_id)

    quality_form = RetentionForm()
    quality_form.init(sm2_card.pk)

    card = get_object_or_404(Card, pk=sm2_card.card.pk)
    
    context = {
        'card': card,
        'form': quality_form
    }
    return render(request, 'cards/review.html', context)

# Display end of review
@login_required
def end_review(request, deck_id):
    deck_manager = DeckManager(deck_id)
    deck = deck_manager.deck
    return render(request, 'cards/end_review.html', {'deck':deck})
