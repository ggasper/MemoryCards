from django.db import models

# Create your models here.

class Deck(models.Model):
    title = models.CharField(max_length=60)
    description = models.TextField()
    # author = models.ForeignKey(User, on_delete=models.CASCADE) TODO
    pub_date = models.DateTimeField('date published')

class Card(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    card_front = models.TextField()
    card_back = models.TextField()
