from django import forms
from pocket_chords.models import Song

EMPTY_VALUE_ITEM = "You can't have an empty list item"

class SongForm(forms.models.ModelForm):

    class Meta:
        model=Song
        fields = ('name', 'text',)
        
        widgets = {
            'name': forms.fields.TextInput(attrs={
                'placeholder': 'Enter an item',
                'class': 'form-control input-lg',
            })
        }
        error_messages = {
            'name': {"required": EMPTY_VALUE_ITEM}
        }