from django import forms
from pocket_chords.models import Song, Sketch

EMPTY__ITEM_ERROR = "You can't have an empty list item"
DUPLICATE_ITEM_ERROR = "This item already exist"

class SongForm(forms.models.ModelForm):

    class Meta:
        model=Song
        fields = ('name', 'text',)
        
        widgets = {
            'name': forms.fields.TextInput(attrs={
                'placeholder': 'Enter an item',
                'class': 'form-control input-lg',
            }), 
        }
        error_messages = {
            'name': {"required": EMPTY__ITEM_ERROR}
        }

class SketchForm(forms.models.ModelForm):

    class Meta:
        model=Sketch
        fields = {'text', 'song'}

        widgets = {
            'text': forms.fields.TextInput(attrs={
                'placeholder': 'Enter an item',
                'class': 'form-control input-lg',
            }), 
        }

        error_messages = {
            'text': {"required": EMPTY__ITEM_ERROR,
                    "unique": DUPLICATE_ITEM_ERROR
                    }
        }

    def clean(self):
        cleaned_data = self.cleaned_data
        song = cleaned_data.get('song')
        text = cleaned_data.get('text')
        if Sketch.objects.filter(song=song, text=text).exists():
            raise forms.ValidationError(DUPLICATE_ITEM_ERROR)
        return cleaned_data