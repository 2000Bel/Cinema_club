from django import forms
from .models import Movie

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'genre', 'year', 'description']
        widgets = {
            'year': forms.DateInput(attrs={'type': 'date'})
        }