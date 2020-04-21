from django.shortcuts import render
import requests
from datetime import datetime
from .models import SummonerV4, MatchlistV4, MatchparticipantV4
from .forms import SummonerForm, SearchForm
from django.db.models import Q

def requestSummonerData(region, summonerName, APIKey):
    URL = "https://" + str(region) + ".api.riotgames.com/lol/summoner/v4/summoners/by-name/" + str(summonerName).replace(" ","").casefold() + "?api_key=" + str(APIKey)
    response = requests.get(URL)
    return response.json()

def requestRankedData(region, ID, APIKey):
    URL = "https://" + str(region) + ".api.riotgames.com/lol/league/v4/entries/by-summoner/" + str(ID) + "?api_key=" + str(APIKey)
    response = requests.get(URL)
    return response.json()


region = "EUW1"
APIKey = 'RGAPI-3852def8-6177-4d52-bb19-bdfbff71b50c'



def player(request):
    # User Input
    global soloRankedData, flexRankedData
    query = request.GET.get('q', '')
    summonerName = query

    sumName = SummonerV4.objects.filter(name__icontains='exkira')

    # Get Real Time User data from Riot API
    responseSummonerData = requestSummonerData(region, summonerName, APIKey)
    ID = responseSummonerData['id']
    accountId = responseSummonerData['accountId']
    responseRankedData = requestRankedData(region, ID, APIKey)

    for queue in responseRankedData:
        if queue['queueType'] == "RANKED_FLEX_SR":
            flexRankedData = {
                'leagueId': queue['leagueId'],
                'tier': queue['tier'],
                'rank': queue['rank'],
                'leaguePoints': queue['leaguePoints'],
                'wins': queue['wins'],
                'losses': queue['losses'],
            }
        elif queue['queueType'] == "RANKED_SOLO_5x5":
            soloRankedData = {
                'leagueId': queue['leagueId'],
                'tier': queue['tier'],
                'rank': queue['rank'],
                'leaguePoints': queue['leaguePoints'],
                'wins': queue['wins'],
                'losses': queue['losses'],
            }

    # Get hours since last game
    lastGamePlayedDate = responseSummonerData['revisionDate'] / 1000.00
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    then = datetime.fromtimestamp(lastGamePlayedDate).strftime('%Y-%m-%d %H:%M:%S')
    diff = datetime.strptime(now, '%Y-%m-%d %H:%M:%S') - datetime.strptime(then, '%Y-%m-%d %H:%M:%S')
    diff_sec = diff.total_seconds()
    lastGamePlayed = int(diff_sec // 3600)

    # Get DB Data on Match History ===============================================
    matchListDB = MatchlistV4.objects.filter(accountid__icontains=accountId)

    matchList = []

    for match in matchListDB:
        gameId = match.gameid

        matchList.append(gameId)

    # All Variables in one place
    context = {
        'responseSummonerData': responseSummonerData,
        'flexRankedData': flexRankedData,
        'soloRankedData': soloRankedData,
        'lastGamePlayed': lastGamePlayed,
        'query':query,
        'matchListDB': matchListDB
    }

    return render(request, 'player/cheatsheet_index.html', context)

def search(request):
    template = 'search/search.html'

    query = request.GET.get('q', '')


    return render(request, template, { 'query': query})
