from django.shortcuts import render
import requests
from datetime import datetime
import time
from .models import SummonerV4, MatchlistV4, MatchparticipantV4
from .forms import SummonerForm, SearchForm
from .dictionaries import queueType, champLinks
import json
import re
import numpy
# Webhook
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import git


def requestSummonerData(region, summonerName, APIKey):
    URL = "https://" + str(region) + ".api.riotgames.com/lol/summoner/v4/summoners/by-name/" + str(summonerName).replace(" ", "").casefold() + "?api_key=" + str(APIKey)
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


def requestMatchTimeline(region, matchId, APIKey):
    URL = "https://" + region + ".api.riotgames.com/lol/match/v4/timelines/by-match/" + str(matchId) + "?api_key=" + str(APIKey)
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


# get summoner spells from ddragon
def getSumSpells():
    sumSpells = requests.get("http://ddragon.leagueoflegends.com/cdn/10.8.1/data/en_US/summoner.json")
    return sumSpells.json()


def getSumSpellLink(sumSpellList, currentCheck):
    for sumSpell, value in sumSpellList:
        if str(currentCheck) == str(value['key']):
            sumSpellLink = "http://ddragon.leagueoflegends.com/cdn/10.8.1/img/spell/" + str(value['image']['full'])
            return sumSpellLink


# get Item .json from DDragon
def getItems():
    items = requests.get("http://ddragon.leagueoflegends.com/cdn/10.8.1/data/en_US/item.json")
    return items.json()


# Get Img for item
def getItemLink(itemList, currentCheck):
    for itemId, value in itemList:
        if str(currentCheck) == itemId:
            itemLink = "http://ddragon.leagueoflegends.com/cdn/10.8.1/img/item/" + str(value['image']['full'])
            return itemLink


# Get Runes
def getRunes():
    runes = requests.get("http://ddragon.leagueoflegends.com/cdn/10.8.1/data/en_US/runesReforged.json")
    return runes.json()


# Get Img for runes
def getRunesLink(runes, primaryTree, currentCheck):
    for runeTree in runes:
        if primaryTree == runeTree['id']:
            for primaryRune in runeTree['slots'][0]['runes']:
                if currentCheck == primaryRune['id']:
                    runesLink = "http://ddragon.leagueoflegends.com/cdn/img/" + str(primaryRune['icon'])
                    return runesLink


# Get img for 2nd Tree
def getSecRunesLink(runes, SecTree):
    for runeTree in runes:
        if SecTree == runeTree['id']:
            runesLink2 = "http://ddragon.leagueoflegends.com/cdn/img/" + str(runeTree['icon'])
            return runesLink2


# get spaces before Capital Letters when needed
def capital_words_spaces(str1):
    return re.sub(r"(\w)([A-Z])", r"\1 \2", str1)


# get Champ .json from DDragon
def getChamps():
    champs = requests.get("http://ddragon.leagueoflegends.com/cdn/10.8.1/data/en_US/champion.json")
    return champs.json()


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


def getFbGiveRate(frames, list):
    for triple in frames:
        for entry in triple['events']:
            if entry['type'] == 'CHAMPION_KILL':
                if entry['victimId'] == participantIdValue:
                    list.append(True)
                    return
                else:
                    return


def getAvgData(allmatches, data):
    list = []
    for entry in allmatches:
        list.append(entry[data])
    # Deal with percentages as strign format
    if type(list[0]) == str:
        floatList = []
        for i in range(len(list)):
            floatList.append(float(list[i].replace("%", "")))
        avgValue = round(numpy.mean(floatList))
    else:
        avgValue = round(numpy.mean(list))
    return avgValue


# DB Functions
def requestMatchlistDB(accountId):
    response = MatchlistV4.objects.filter(accountId__icontains=accountId)


region = "EUW1"
APIKey = 'RGAPI-9d293140-6046-48b1-9fc9-3c6b34a151a5'




testMatchList = requestMatchlistDB('KCZb4c6duEOJBDxjEK6TVki-mjjt3LJZC5mWCX-hKm6Xcw')







