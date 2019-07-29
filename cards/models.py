from django.db import models
from django.contrib.auth.models import User

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
