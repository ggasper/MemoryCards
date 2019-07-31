from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.utils import timezone

from .models import Card, Deck, SM2_data
from .forms import DeckForm, DeckEditForm, CardEditForm, RetentionForm
from .sm2 import SM2

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


# Form for editing the deck
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
        
    deck_form = DeckEditForm()
    deck_form.init(deck)
    card_form = CardEditForm()
    card_form.init(card)

    # Find next and previous card
    n_cards = deck.card_set.filter(pk__gt = card.pk)
    p_cards = deck.card_set.filter(pk__lt = card.pk).order_by('-pk')

    if len(n_cards) <= 0:
        n_card = deck.card_set.create(front="", back="")
    else:
        n_card = n_cards[0]

    context = {
        'deck_form': deck_form,
        'card_form': card_form,
        'deck': deck,
        'n_card': n_card
    }
        
    if len(p_cards) > 0:
        p_card = p_cards[0]
        context['p_card'] = p_card
        
    return render(request, 'cards/edit_deck.html', context)

# Display deck for learning with sm2 algorithm
def review(request, deck_id):
    sm2 = SM2(request.user, deck_id)

    # Check if we are starting new repeat
    if request.method == 'GET' and 'new' in request.GET and request.GET['new']:
        sm2.start_repeat()
    
    # If we have some data to update first process that
    if request.method == 'POST':
        form = RetentionForm(request.POST)
        if form.is_valid():
            quality = int(form.cleaned_data['quality'][0])
            #print(quality)
            sm2_data_id = int(form.cleaned_data['sm2_data_id'])

            sm2_data = get_object_or_404(SM2_data, pk=sm2_data_id)

            # The repetition counter equals zero if we got here from inital repetition and something else if we are just repeating bad
            # attempts.
            if sm2_data.repetition_counter <= 0:
                sm2.update_card(sm2_data.card, quality)
            else:
                sm2.update_card_bq(sm2_data.card, quality)
    # Get new card if there is one
    sm2_card = sm2.get_card()

    # If there is no card that hasn't been reviewed yet choose one from poorly graded ones
    if not sm2_card:
        sm2_card = sm2.get_card_bq()
    # If there is still no card we are done... root is a placeholder
    if not sm2_card:
        return redirect('/')

    quality_form = RetentionForm()
    quality_form.init(sm2_card.pk)

    card = get_object_or_404(Card, pk=sm2_card.card.pk)
    
    context = {
        'card': card,
        'form': quality_form
    }
    return render(request, 'cards/review.html', context)
