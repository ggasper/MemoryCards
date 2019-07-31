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

# A form for rating retention
class RetentionForm(forms.Form):
    OPTIONS = (
        (5, 'perfect'),
        (4, 'great'),
        (3, 'ok'),
        (2, 'close'),
        (1, 'wrong'),
        (0, 'blank')
    )
    quality = forms.MultipleChoiceField(choices=OPTIONS, widget=forms.CheckboxSelectMultiple())
    sm2_data_id = forms.IntegerField(widget=forms.HiddenInput())

    def init(self, sm2_data_id):
        self.fields['sm2_data_id'].initial = sm2_data_id
