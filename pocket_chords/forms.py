from django import forms
from pocket_chords.models import Song, Sketch

EMPTY__ITEM_ERROR = "You can't have an empty list item"
DUPLICATE_ITEM_ERROR = "Item already exists in the model"


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
            'text': {"required": EMPTY__ITEM_ERROR}
            }
    
    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get('text')
        song = cleaned_data.get('song')
        if Sketch.objects.filter(song=song, text=text).exists():
            raise forms.ValidationError((DUPLICATE_ITEM_ERROR), code='duplicate value')
        return cleaned_data

class NewSongForm(SongForm):
    
    def save(self, owner):
        if owner.is_authenticated:
            Song.create_new(first_item_name=self.cleaned_data['name'],
                            owner=owner)
        else:
            Song.create_new(first_item_name=self.cleaned_data['name'])