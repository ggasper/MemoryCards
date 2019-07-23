from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Deck(models.Model):
    title = models.CharField(max_length=60)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    # author = models.ForeignKey(User, on_delete=models.CASCADE) TODO
    pub_date = models.DateTimeField('date published')

class Card(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    front = models.TextField()
    back = models.TextField()
