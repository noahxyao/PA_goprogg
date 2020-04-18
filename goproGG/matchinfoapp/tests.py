from django.test import TestCase
from django.shortcuts import render
import requests
from datetime import datetime
from .models import Summoner
from .forms import SummonerForm

# Create your tests here.

def index(request):
    def requestSummonerData(region, summonerName, APIKey):
        URL = "https://" + str(region) + ".api.riotgames.com/lol/summoner/v4/summoners/by-name/" + str(summonerName).replace(" ","").casefold() + "?api_key=" + str(APIKey)
        response = requests.get(URL)
        return response.json()

    region = "EUW1"
    summonerNameList = Summoner.objects.all() #return all summoners in django database created in models
    print(summonerNameList)
    APIKey = 'RGAPI-d6979fea-d983-4285-b6c1-72b674ac39b1'

    for summonerName in summonerNameList:
        responseSummonerData = requestSummonerData(region, summonerName, APIKey)
        ID = responseSummonerData['id']
        responseRankedData = requestRankedData(region, ID, APIKey)

    return render(request, 'ranked/weather_index.html')