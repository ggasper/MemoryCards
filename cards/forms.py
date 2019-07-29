from django import forms

# A form for creating a deck
class DeckForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100)
    description = forms.CharField(label='Description')

# A form for editing a deck
class DeckEditForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100)
    description = forms.CharField(label='Description')

    def init(self, deck):
        self.fields['title'].initial = deck.title
        self.fields['description'].initial = deck.description

# A form for editing a specific card
class CardEditForm(forms.Form):
    front = forms.CharField(label='Front')
    back = forms.CharField(label='Back')

    def init(self, card):
        self.fields['front'].initial = card.front
        self.fields['back'].initial = card.back
