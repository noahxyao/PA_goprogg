import forms
from .models import SummonerV4

class SummonerForm(forms.ModelForm):
    class Meta:
        model = SummonerV4
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class' : 'input', 'placeholder' : 'Summoner Name'}),
        } #updates the input class to have the correct Bulma class and placeholder

class SearchForm(forms.Form):
    sumName = forms.CharField()