import requests
from datetime import datetime
from dictionaries import champLinks

import json

def requestSummonerData(region, summonerName, APIKey):
    URL = "https://" + str(region) + ".api.riotgames.com/lol/summoner/v4/summoners/by-name/" + str(summonerName).replace(" ","").casefold() + "?api_key=" + str(APIKey)
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

def getChampLink(champLinks, currentCheck):
    for name, link in champLinks:
        if str(currentCheck) == name:
            champLink = link
            return champLink

region = "EUW1"
APIKey = 'RGAPI-15aafca3-6a5d-4e73-a912-9ad6cf249e39'
summonerName = 'exkira'

responseSummonerData = requestSummonerData(region, summonerName, APIKey)
ID = responseSummonerData['id']
accountId = responseSummonerData['accountId']

responseMatchList = requestMatchList(region, accountId, APIKey)

matchList_data = []

for i in range(3):
    matchListInfo = {
        # 'gameId': responseMatchList['matches'][i]['gameId'],
        # 'champion': responseMatchList['matches'][i]['champion'],
        # # 'championName': getChampName(champions['data'].items(), responseMatchList['matches'][i]['champion']),
        # # 'championLink': getChampLink(champLinks.items(),responseMatchList['matches'][i]['champion']),
        # 'queue': responseMatchList['matches'][i]['queue'],
        # 'queueType': queueType[str(responseMatchList['matches'][i]['queue'])],
        # 'season': responseMatchList['matches'][i]['season'],
        # 'timestamp': responseMatchList['matches'][i]['timestamp'],
        # 'lastGame': requestLastGamePlayed(responseMatchList['matches'][i]['timestamp']),
        # 'role':responseMatchList['matches'][i]['role'],
        # 'lane': responseMatchList['matches'][i]['lane'],
        # API response for match Details
        'matchDetailInfo': requestMatchInfo(region, responseMatchList['matches'][i]['gameId'], APIKey),
    }


    matchListInfo.update( {
            'participant_1_champLink': getChampLink(champLinks.items(),matchListInfo['matchDetailInfo']['participants'][0]['championId'])
        })

    matchList_data.append(matchListInfo)

print(matchList_data[1]['matchDetailInfo']['participants'][0]['championId'])
print(matchList_data[1]['participant_1_champLink'])