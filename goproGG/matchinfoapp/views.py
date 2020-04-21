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

def requestMatchList(region, accountId, APIKey):
    URL = "https://" + region + ".api.riotgames.com/lol/match/v4/matchlists/by-account/" + str(accountId) + "?api_key=" + str(APIKey)
    response = requests.get(URL)
    return response.json()

def requestMatchInfo(region, matchId, APIKey):
    URL = "https://" + region + ".api.riotgames.com/lol/match/v4/matches/" + str(matchId) + "?api_key=" + str(APIKey)
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
    responseMatchList = requestMatchList(region, accountId, APIKey)


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

    # For 20 games, get matchIds along with all match data in one dictionary ===============================================
    matchList_data = []
    matchDetail_data = []

    for i in range(20):
        matchListInfo = {
            'gameId': responseMatchList['matches'][i]['gameId'],
            'champion': responseMatchList['matches'][i]['champion'],
            'queue': responseMatchList['matches'][i]['queue'],
            'season': responseMatchList['matches'][i]['season'],
            'timestamp': responseMatchList['matches'][i]['timestamp'],
            'role':responseMatchList['matches'][i]['role'],
            'lane': responseMatchList['matches'][i]['lane'],
            'matchDetailInfo': requestMatchInfo(region, responseMatchList['matches'][i]['gameId'], APIKey)
        }

        matchList_data.append(matchListInfo)




    # All Variables in one place
    context = {
        'responseSummonerData': responseSummonerData,
        'flexRankedData': flexRankedData,
        'soloRankedData': soloRankedData,
        'lastGamePlayed': lastGamePlayed,
        'query':query,
        'matchList_data': matchList_data,
        'matchDetail_data': matchDetail_data,
        'responseMatchList': responseMatchList,
    }

    return render(request, 'player/cheatsheet_index.html', context)

def search(request):
    template = 'search/search.html'

    query = request.GET.get('q', '')


    return render(request, template, { 'query': query})
