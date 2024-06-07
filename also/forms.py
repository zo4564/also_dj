from django import forms
from .models import Species

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class SpeciesForm(forms.ModelForm):
    class Meta:
        model = Species
        fields = ['species_name', 'species_genome', 'species_description', 'can_move', 'can_defend', 'image']
        widgets = {
            'species_name': forms.TextInput(attrs={'placeholder': 'Podaj nazwę gatunku'}),
            'species_genome': forms.TextInput(attrs={'placeholder': 'Podaj genom'}),
            'species_description': forms.TextInput(attrs={'placeholder': 'Napisz krótki opis'}),
            'can_move': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'can_defend': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
        }
