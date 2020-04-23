from django.shortcuts import render
import requests
from datetime import datetime
from .models import SummonerV4, MatchlistV4, MatchparticipantV4
from .forms import SummonerForm, SearchForm
from .dictionaries import queueType, champLinks
import json
import re

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

# Get hours since last game
def requestLastGamePlayed(timestamp):
    lastGamePlayedDate = timestamp / 1000.00
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    then = datetime.fromtimestamp(lastGamePlayedDate).strftime('%Y-%m-%d %H:%M:%S')
    diff = datetime.strptime(now, '%Y-%m-%d %H:%M:%S') - datetime.strptime(then, '%Y-%m-%d %H:%M:%S')
    diff_sec = diff.total_seconds()
    lastGamePlayed = int(diff_sec // 3600)
    return lastGamePlayed

#get Champ .json from DDragon
def getChamps():
    champs = requests.get("http://ddragon.leagueoflegends.com/cdn/10.8.1/data/en_US/champion.json")
    return champs.json()

#get spaces before Capital Letters when needed
def capital_words_spaces(str1):
    return re.sub(r"(\w)([A-Z])", r"\1 \2", str1)

# Turn champion ID into acutal name
def getChampName(champList, currentCheck):
    for name, champEntry in champList:
        if str(currentCheck) == champEntry['key']:
            champName = name
            return capital_words_spaces(champName)

# Turn champion ID into link to square image
def getChampLink(champLinks, currentCheck):
	for name, link in champLinks:
		if str(currentCheck) == name:
			champLink = link
			return champLink


region = "EUW1"
APIKey = 'RGAPI-15aafca3-6a5d-4e73-a912-9ad6cf249e39'



def player(request):
    # Define some global variables to use later
    global soloRankedData, flexRankedData, soloRankedContext, flexRankedContext
    # User Input
    query = request.GET.get('q', '')
    summonerName = query

    sumName = SummonerV4.objects.filter(name__icontains='exkira')

    # Get Real Time User data from Riot API, get all champ data from DDragon
    responseSummonerData = requestSummonerData(region, summonerName, APIKey)
    ID = responseSummonerData['id']
    accountId = responseSummonerData['accountId']
    responseRankedData = requestRankedData(region, ID, APIKey)
    responseMatchList = requestMatchList(region, accountId, APIKey)
    champions = getChamps()



    # Winrates in both Queues
    if bool(responseRankedData) == True:
        # Save Ranked Data in dicts
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

        if bool(soloRankedData)== True:
            soloqWR = "{0:.0%}".format(soloRankedData['wins']/(soloRankedData['wins'] + soloRankedData['losses']))
        else:
            soloqWR = "Unranked"

        if bool(flexRankedData) == True:
            flexqWR = "{0:.0%}".format(flexRankedData['wins'] / (flexRankedData['wins'] + flexRankedData['losses']))
        else:
            flexqWR = "Unranked"
    else:
        soloqWR = "Unranked"
        flexqWR = "Unranked"

   # For limit = 20 games, get matchIds along with all match data in one dictionary ===============================================
    matchList_data = []
    matchDetail_data = []

    index = 0
    limit = 20

    for i in range(len(responseMatchList['matches'])):

        matchListInfo = {
            'gameId': responseMatchList['matches'][i]['gameId'],
            'champion': responseMatchList['matches'][i]['champion'],
            'championName': getChampName(champions['data'].items(), responseMatchList['matches'][i]['champion']),
            'championLink': getChampLink(champLinks.items(),responseMatchList['matches'][i]['champion']),
            'queue': responseMatchList['matches'][i]['queue'],
            'queueType': queueType[str(responseMatchList['matches'][i]['queue'])],
            'season': responseMatchList['matches'][i]['season'],
            'timestamp': responseMatchList['matches'][i]['timestamp'],
            'lastGame': requestLastGamePlayed(responseMatchList['matches'][i]['timestamp']),
            'role':responseMatchList['matches'][i]['role'],
            'lane': responseMatchList['matches'][i]['lane'],
            'matchDetailInfo': requestMatchInfo(region, responseMatchList['matches'][i]['gameId'], APIKey)
        }


        matchList_data.append(matchListInfo)
        index += 1
        if index == limit:
            break

    # Get SoloQ and flexQ last game played
    lastSoloQGame = 'Longer than 20 Games ago'
    lastFlexQGame = 'Longer than 20 games ago'
    for entry in matchList_data:
        if entry['queue'] == 420:
            lastSoloQGame = 'Last Played: ' + str(entry['lastGame']) + ' hours ago'
            break

        if entry['queue'] == 440:
            lastFlexQGame = 'Last Played: ' + str(entry['lastGame']) + ' hours ago'
            break





    # All Variables in one place
    context = {
        'responseSummonerData': responseSummonerData,
        # 'flexRankedData': flexRankedData,
        # 'soloRankedData': soloRankedData,
        'query':query,
        'matchList_data': matchList_data,
        'matchDetail_data': matchDetail_data,
        'responseMatchList': responseMatchList,
        'lastSoloQGame': lastSoloQGame,
        'lastFlexQGame': lastFlexQGame,
        'soloqWR': soloqWR,
        'flexqWR': flexqWR,
    }

    if bool(responseRankedData)== True:
        context.update({'soloRankedData': soloRankedData,})
        context.update({'flexRankedData': flexRankedData, })


    return render(request, 'player/cheatsheet_index.html', context)

def search(request):
    template = 'search/search.html'

    query = request.GET.get('q', '')


    return render(request, template, { 'query': query})
