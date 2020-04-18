from django.forms import ModelForm, TextInput
from .models import Summoner

class SummonerForm(ModelForm):
    class Meta:
        model = Summoner
        fields = ['name']
        widgets = {
            'name': TextInput(attrs={'class' : 'input', 'placeholder' : 'Summoner Name'}),
        } #updates the input class to have the correct Bulma class and placeholder