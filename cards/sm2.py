from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from .models import Deck, Card, SM2_data

# SM2 Algorithm on a deck
class SM2:
    def __init__(self, user, deck_id):
        self.deck = get_object_or_404(Deck, pk = deck_id)
        self.user = user

        # Check if user has sm2 objects for every card. If not create them
        for card in self.deck.card_set.all():
            if SM2_data.objects.filter(user=self.user, card=card).count() == 0:
                SM2_data.objects.create(user=self.user, card=card).save()
                
        
        
    def start_repeat(self):
        # retrieve all sm2 data objects and decrease repetitions by 1
        data = SM2_data.objects.filter(user=self.user, card__deck=self.deck)
        for value in data:
            value.repetition_counter -= 1
            value.save()

    # Get a card for repetition
    def get_card(self):
        sm2_card_data = SM2_data.objects.filter(user=self.user, repetition_counter__lte=0, card__deck=self.deck)
        if len(sm2_card_data) > 0:
            return sm2_card_data[0]
    
    # Get a card with a score below 3   
    def get_card_bq(self):
       sm2_card_data = SM2_data.objects.filter(user=self.user, last_score__lt=3, card__deck=self.deck)
       if len(sm2_card_data) > 0:
           return sm2_card_data[0]
     
    def update_card(self, card, quality):
        sm2_data = get_object_or_404(SM2_data, card=card, user=self.user)
        sm2_data.last_score = quality
        if quality < 3:
            sm2_data.repetition = 1
            sm2_data.repetition_counter = 1
        else:
            sm2_data.EF = sm2_data.EF + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
            if sm2_data.EF < 1.3:
                sm2_data.EF = 1.3
            
            def new_repeats(repeat):
                if repeat <= 1:
                    return 1
                elif repeat == 2:
                    return 6
                else:
                    return sm2_data.EF * new_repeats(repeat - 1)
            
            sm2_data.repetition = new_repeats(sm2_data.repetition)
            sm2_data.repetition_counter = sm2_data.repetition
        sm2_data.save()
        
    def update_card_bq(self, card, quality):
        sm2_data = get_object_or_404(SM2_data, card=card, user=self.user)
        sm2_data.last_score = quality
        sm2_data.save()
