from .models import Deck, Card
from django.shortcuts import get_object_or_404, redirect

class DeckManager:
    @staticmethod
    def new_blank_card(deck):
        return deck.card_set.create(front="", back="")

    @staticmethod
    def new_deck_from_form(form):
        title = form.cleaned_data['title']
        description = form.cleaned_data['description']
        deck = Deck(title=title, author=request.user, description=description, pub_date=timezone.now())
        deck.save()
        
        # Allow the user to edit their own decks
        deck.allow_edit(request.user)
        
        card = new_blank_card(deck)

        return redirect('cards:edit', card_id=card.pk, deck_id=deck.pk)

    def deck_from_id(self, deck_id):
        return get_object_or_404(Deck, pk=deck_id)
    
    def __init__(self, deck_id):
        self.deck = self.deck_from_id(deck_id)

    def get_next_card(self, card):
        n_cards = self.deck.card_set.filter(pk__gt=card.pk).order_by('pk')
        if len(n_cards) > 0:
            return n_cards[0]
        else:
            return Card(pk=0, front="", back="")

    def get_previous_card(self, card):
        p_cards = self.deck.card_set.filter(pk__lt=card.pk).order_by('-pk')
        if len(p_cards) > 0:
            return p_cards[0]

    def get_first_card(self):
        cards = self.deck.card_set.order_by('pk')
        if len(cards) > 0:
            return cards[0]
        
    def get_cards_around(self, card):
        num_cards = 5
        cards = self.deck.card_set.order_by('pk')
        i = list(cards).index(card)

        start = max(i - num_cards, 0)

        pages = []
        
        for j in range(num_cards * 2 + 1):
            if start + j >= len(cards):
                break
            pages.append((start + j + 1, cards[start + j]))
        return pages
