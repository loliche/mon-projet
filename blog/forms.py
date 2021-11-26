from django import forms
from .models import Animal

class MoveForm(forms.ModelForm):
 
    class Meta:
        model = Animal
        fields = ('lieu',)

class PostForm(forms.ModelForm):

    class Meta:
        model = Animal
        fields = ('id_animal', 'type', 'race', 'photo',)