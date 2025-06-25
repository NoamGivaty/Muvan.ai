from django import forms

class RecipeURLForm(forms.Form):
    url = forms.URLField(label='Recipe URL', widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Paste recipe URL here...'}))
