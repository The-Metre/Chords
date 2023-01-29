from django import forms
from pocket_chords.models import Song, Sketch

EMPTY__ITEM_ERROR = "You can't have an empty list item"
DUPLICATE_ITEM_ERROR = 'The chunk already exist. Please change your input and try again.'

class SongForm(forms.models.ModelForm):

    class Meta:
        model=Song
        fields = ('name',)
        
        widgets = {
            'name': forms.fields.TextInput(attrs={
                'placeholder': 'Enter an item',
                'class': 'form-control input-lg',
            }), 
        }

        labels = {
            'name': ""
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
                'placeholder': 'Enter a song item',
                'class': 'form-control input-lg',
            }),
            'song': forms.HiddenInput()
        }
        labels = {
            'text': "",
            'song': ""
        }

        error_messages = {
            'text': {"required": EMPTY__ITEM_ERROR,
                    "unique": DUPLICATE_ITEM_ERROR
                    }
        }
    
    def clean_text(self):
        cleaned_data = self.cleaned_data
        text = cleaned_data['text']
        song = cleaned_data['song']
        if Sketch.objects.filter(song=song, text=text).exists():
            raise forms.ValidationError((f'({text}) sticker already exist in the song'), code='duplicate value' )
        return cleaned_data