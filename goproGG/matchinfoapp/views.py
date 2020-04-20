from django.shortcuts import render
import requests
from datetime import datetime
from .models import SummonerV4
from .forms import SummonerForm

def requestSummonerData(region, summonerName, APIKey):
    URL = "https://" + str(region) + ".api.riotgames.com/lol/summoner/v4/summoners/by-name/" + str(summonerName).replace(" ","").casefold() + "?api_key=" + str(APIKey)
    response = requests.get(URL)
    return response.json()

def requestRankedData(region, ID, APIKey):
    URL = "https://" + str(region) + ".api.riotgames.com/lol/league/v4/entries/by-summoner/" + str(ID) + "?api_key=" + str(APIKey)
    response = requests.get(URL)
    return response.json()


region = "EUW1"
APIKey = 'RGAPI-a84d98d6-747a-4382-bee5-3a024dd98f50'



def index(request):
    summonerNameList = SummonerV4.objects.all() #['minras', 'exkira', 'eksrag']  # return all summoners in django database created in models
    # Form: POST related
    if request.method == 'POST':  # only true if form is submitted
        form = SummonerForm(request.POST)  # add actual request data to form for processing
        form.save()  # will validate and save if validate

    # Form
    form = SummonerForm()

    summoner_data = []

    for summonerName in summonerNameList:
        responseSummonerData = requestSummonerData(region, summonerName.name, APIKey)
        ID = responseSummonerData['id']
        responseRankedData = requestRankedData(region, ID, APIKey)

        # Get hours since last game
        lastGamePlayedDate = responseSummonerData['revisionDate'] / 1000.00
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        then = datetime.fromtimestamp(lastGamePlayedDate).strftime('%Y-%m-%d %H:%M:%S')
        diff = datetime.strptime(now, '%Y-%m-%d %H:%M:%S') - datetime.strptime(then, '%Y-%m-%d %H:%M:%S')
        diff_sec = diff.total_seconds()
        lastGamePlayed = int(diff_sec // 3600)

        summoner = {
            'name': responseSummonerData['name'],
            'id': responseSummonerData['id'],
            'accountId': responseSummonerData['accountId'],
            'puuid': responseSummonerData['puuid'],
            'profileIconId': responseSummonerData['profileIconId'],
            'revisionDate': responseSummonerData['revisionDate'],
            'summonerLevel': responseSummonerData['summonerLevel']
        }

        summoner_data.append(summoner)  # add the data for current summoner into our list


    # All Variables in one place
    context = {
        'data': responseSummonerData,
        'data2': responseRankedData,
        'lastGamePlayed': lastGamePlayed,
        'form': form,
        'summoner_data': summoner_data
    }

    return render(request, 'ranked/cheatsheet_index.html', context)