from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

from guardian.shortcuts import assign_perm

# Create your models here.

class Deck(models.Model):
    title = models.CharField(max_length=60)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    pub_date = models.DateTimeField('date published')

    class Meta:
        permissions = (
            ('can_edit', 'Can edit'),
        )

    def allow_edit(self, user):
        assign_perm('can_edit', user, self)

    def update_from_form(self, form):
        if form.is_valid():
            self.title = form.cleaned_data['title']
            self.description = form.cleaned_data['description']
            self.save()
            return True
        return False

class Card(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    front = models.TextField()
    back = models.TextField()

    def update_from_form(self, form):
        print("updating card")
        if form.is_valid():
            self.front = form.cleaned_data['front']
            self.back = form.cleaned_data['back']
            self.save()
            return True
        return False

class SM2_data(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)

    last_score = models.PositiveIntegerField(default=5, validators=[MinValueValidator(0), MaxValueValidator(5)])
    EF = models.FloatField(default=2.5)
    repetition = models.IntegerField(default=1)
    repetition_counter = models.IntegerField(default=1)
    
    class Meta:
        unique_together = ('user', 'card',)
        
    def needs_review(self):
        return self.repetition_counter <= 0
