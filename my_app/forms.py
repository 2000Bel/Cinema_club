from django import forms
from .models import Movie

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'genre', 'year', 'description', 'poster_url', 'rating']
        widgets = {
            'year': forms.DateInput(attrs={'type': 'date'}),
            'rating': forms.Select(choices=[(i, f'{i} Star{"s" if i > 1 else ""}') for i in range(1, 6)])
        }