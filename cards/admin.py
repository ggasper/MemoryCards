from django.contrib import admin
from .models import Deck, Card, SM2_data

# Register your models here.

admin.site.register(Deck)
admin.site.register(Card)
admin.site.register(SM2_data)
