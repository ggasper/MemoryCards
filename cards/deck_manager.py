from .models import Deck, Card
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.contrib.postgres.search import SearchVector, SearchRank, SearchQuery

class DeckManager:
    @staticmethod
    def new_blank_card(deck):
        return deck.card_set.create(front="", back="")

    @staticmethod
    def new_deck_from_form(request, form):
        title = form.cleaned_data['title']
        description = form.cleaned_data['description']
        deck = Deck(title=title, author=request.user, description=description, pub_date=timezone.now())
        deck.save()
        
        # Allow the user to edit their own decks
        deck.allow_edit(request.user)
        
        card = DeckManager.new_blank_card(deck)

        return redirect('cards:edit', card_id=card.pk, deck_id=deck.pk)

    @staticmethod
    def get_decks(page_num, author=None, per_page=40, query=None):
        # If there is an author only return his own decks
        if not author:
            deck_query = Deck.objects.order_by('-pub_date')
        else:
            deck_query = Deck.objects.filter(author=author).order_by('pub_date')
        
        # If there is a query process it
        if query:
            vector = SearchVector('title', weight='A') + SearchVector('description', weight='B')
            search_query = SearchQuery(query)
            deck_list = deck_query.annotate(rank=SearchRank(vector, search_query)).filter(rank__gte=0.3).order_by('-rank')
        else:
            deck_list = deck_query.all()

        
            
        start = (page_num - 1) * per_page
        decks = []
        for i in range(start, start + per_page):
            if i >= len(deck_list):
                break
            decks.append(deck_list[i])
        first_page = max(1, page_num - 5)
        last_page = min(first_page + 11, (len(deck_list) + (per_page - len(deck_list)) % per_page) // per_page)
        return (decks, first_page, last_page)

    def can_edit(self, user):
        return self.deck.can_edit(user)
    
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
