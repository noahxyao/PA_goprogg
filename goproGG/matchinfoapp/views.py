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

#get summoner spells from ddragon
def getSumSpells():
    sumSpells = requests.get("http://ddragon.leagueoflegends.com/cdn/10.8.1/data/en_US/summoner.json")
    return sumSpells.json()

def getSumSpellLink(sumSpellList, currentCheck):
    for sumSpell, value in sumSpellList:
        if str(currentCheck) == str(value['key']):
            sumSpellLink = "http://ddragon.leagueoflegends.com/cdn/10.8.1/img/spell/" + str(value['image']['full'])
            return sumSpellLink

#get Item .json from DDragon
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

#get spaces before Capital Letters when needed
def capital_words_spaces(str1):
    return re.sub(r"(\w)([A-Z])", r"\1 \2", str1)

#get Champ .json from DDragon
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

region = "EUW1"
APIKey = 'RGAPI-9d293140-6046-48b1-9fc9-3c6b34a151a5'



def player(request):
    # Define some global variables to use later
    global soloRankedData, flexRankedData, soloRankedContext, flexRankedContext, participantIdValue
    # User Input
    query = request.GET.get('q', '')
    summonerName = query

    # manually enter sumName without search box
    sumName = SummonerV4.objects.filter(name__icontains='exkira')

    # Get Real Time User data from Riot API, get all champ data from DDragon
    responseSummonerData = requestSummonerData(region, summonerName, APIKey)
    ID = responseSummonerData['id']
    accountId = responseSummonerData['accountId']
    responseRankedData = requestRankedData(region, ID, APIKey)
    responseMatchList = requestMatchList(region, accountId, APIKey)
    champions = getChamps()
    items = getItems()
    sumSpells = getSumSpells()
    runes = getRunes()



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
        soloqWR = "unavailable | Unranked"
        flexqWR = "unavailable | Unranked"

    # For limit = 20 games, get matchIds along with all match data in one dictionary ===============================================
    index = 0
    limit = 20

    # Declare variables to be used outside the individual matches
    matchList_data = []
    matchDetail_data = []
    fbList = []
    fbGiveList = []
    rangeTen = [1,2,3,4,5,6,7,8,9,10]

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
            # API response for match Details
            'matchDetailInfo': requestMatchInfo(region, responseMatchList['matches'][i]['gameId'], APIKey),
            'matchTimeline': requestMatchTimeline(region, responseMatchList['matches'][i]['gameId'], APIKey),
        }

        # Get champ pictures for all participants of same game
        matchListInfo.update({
            "champLink_1": getChampLink(champLinks.items(),matchListInfo['matchDetailInfo']['participants'][0]['championId']),
            "champLink_2": getChampLink(champLinks.items(),matchListInfo['matchDetailInfo']['participants'][1]['championId']),
            "champLink_3": getChampLink(champLinks.items(),matchListInfo['matchDetailInfo']['participants'][2]['championId']),
            "champLink_4": getChampLink(champLinks.items(),matchListInfo['matchDetailInfo']['participants'][3]['championId']),
            "champLink_5": getChampLink(champLinks.items(),matchListInfo['matchDetailInfo']['participants'][4]['championId']),
            "champLink_6": getChampLink(champLinks.items(),matchListInfo['matchDetailInfo']['participants'][5]['championId']),
            "champLink_7": getChampLink(champLinks.items(),matchListInfo['matchDetailInfo']['participants'][6]['championId']),
            "champLink_8": getChampLink(champLinks.items(),matchListInfo['matchDetailInfo']['participants'][7]['championId']),
            "champLink_9": getChampLink(champLinks.items(),matchListInfo['matchDetailInfo']['participants'][8]['championId']),
            "champLink_10": getChampLink(champLinks.items(),matchListInfo['matchDetailInfo']['participants'][9]['championId']),
            }
        )

        # Get match information summoner by finding participantId list number 0-9 from result JSON
        participantCounter = 0
        for participant in matchListInfo['matchDetailInfo']['participantIdentities']:
            if participant['player']['summonerName'] == responseSummonerData['name']:
                participantId = participantCounter
                participantIdValue = participantId + 1
                # Add Team Id for specific stats
                if participantId <5:
                    teamId = 0
                else:
                    teamId = 1
            else:
                participantCounter += 1

        # Get match result for summoner's participantId
        if matchListInfo['matchDetailInfo']['participants'][participantId]['stats']['win'] == True:
            matchListInfo.update({"result": 'Victory'})
        else:
            matchListInfo.update({"result": 'Defeat'})

        # Add Multikills
        if matchListInfo['matchDetailInfo']['participants'][participantId]['stats']['largestMultiKill'] > 1:
            killDict = {'2': 'Doublekill',
                        '3': 'Triplekill',
                        '4': 'Quadrakill',
                        '5': 'Pentakill',
                        }
            matchListInfo.update({'largestMultiKill': killDict[str(matchListInfo['matchDetailInfo']['participants'][participantId]['stats']['largestMultiKill'])]})

        # Add total CS
        totalCS = matchListInfo['matchDetailInfo']['participants'][participantId]['stats']['totalMinionsKilled'] + matchListInfo['matchDetailInfo']['participants'][participantId]['stats']['neutralMinionsKilled']
        matchListInfo.update({'totalCS': totalCS})

        # Add Game Duration and duration related variables
        gameDuration = matchListInfo['matchDetailInfo']['gameDuration']
        gameDurationMin = time.strftime('%M', time.gmtime(gameDuration))
        gameDurationSec = time.strftime('%S', time.gmtime(gameDuration))
        # cs per min
        cspMin = round(totalCS/(int(gameDurationMin) + int(gameDurationSec)/60),2)
        # dmg per min
        dpm = round(matchListInfo['matchDetailInfo']['participants'][participantId]['stats']['totalDamageDealtToChampions'] / (int(gameDurationMin) + int(gameDurationSec)/60),2)
        matchListInfo.update({'gameDurationMin': gameDurationMin,
                              'gameDurationSec': gameDurationSec,
                              'cspMin': cspMin,
                              'dpm': dpm,
                              })

        # Adding Team KDA
        team1Kills = 0
        team1Deaths = 0
        team1Assists = 0
        team2Kills = 0
        team2Deaths = 0
        team2Assists = 0
        team1Kda = [team1Kills, team1Deaths, team1Assists]
        team2Kda = [team2Kills, team2Deaths, team2Assists]
        teamKdaList = [team1Kda, team2Kda]

        for participantKills in range(5):
            teamKdaList[0][0] += matchListInfo['matchDetailInfo']['participants'][participantKills]['stats']['kills']
            teamKdaList[0][1] += matchListInfo['matchDetailInfo']['participants'][participantKills]['stats']['deaths']
            teamKdaList[0][2] += matchListInfo['matchDetailInfo']['participants'][participantKills]['stats']['assists']
        for participantKills in range(5, 10):
            teamKdaList[1][0] += matchListInfo['matchDetailInfo']['participants'][participantKills]['stats']['kills']
            teamKdaList[1][1] += matchListInfo['matchDetailInfo']['participants'][participantKills]['stats']['deaths']
            teamKdaList[1][2] += matchListInfo['matchDetailInfo']['participants'][participantKills]['stats']['assists']

            matchListInfo.update({'team1Kills': teamKdaList[0][0],
                                  'team1Deaths': teamKdaList[0][1],
                                  'team1Assists': teamKdaList[0][2],
                                  'team2Kills': teamKdaList[1][0],
                                  'team2Deaths': teamKdaList[1][1],
                                  'team2Assists': teamKdaList[1][2],
                                  })

        # Adding KillParticipation
        teamKills1 = 0
        teamKills2 = 0
        teamKillsList = [teamKdaList[0][0], teamKdaList[1][0]]

        try:
            killPart = round((matchListInfo['matchDetailInfo']['participants'][participantId]['stats']['kills'] + matchListInfo['matchDetailInfo']['participants'][participantId]['stats']['assists'])/teamKillsList[teamId], 2)
            matchListInfo.update({'killPart': "{0:.0%}".format(killPart)})
        except ZeroDivisionError:
            killPart = "No Kills"
            matchListInfo.update({'killPart': killPart})

        # Dmg Participation: Dmg Dealt to Champions
        team1DamageChamps = 0
        team2DamageChamps = 0
        teamDmgChampsList = [team1DamageChamps, team2DamageChamps]

        for participantDmg in range(5):
            teamDmgChampsList[0] += matchListInfo['matchDetailInfo']['participants'][participantDmg]['stats']['totalDamageDealtToChampions']
        for participantDmg in range(5,10):
            teamDmgChampsList[1] += matchListInfo['matchDetailInfo']['participants'][participantDmg]['stats']['totalDamageDealtToChampions']

        try:
            dmgPart = round(matchListInfo['matchDetailInfo']['participants'][participantId]['stats']['totalDamageDealtToChampions'] / teamDmgChampsList[teamId],2)
            matchListInfo.update({'dmgPart': "{0:.0%}".format(dmgPart)})
        except ZeroDivisionError:
            dmgPart = "No Dmg dealt"
            matchListInfo.update({'dmgPart': dmgPart})


        # Dmg Dealt to Turret Percentage in Team
        team1DamageTurrets = 0
        team2DamageTurrets = 0
        teamTurretDmgList = [team1DamageTurrets, team2DamageTurrets]

        for participantDmg in range(5):
            teamTurretDmgList[0] += matchListInfo['matchDetailInfo']['participants'][participantDmg]['stats']['damageDealtToTurrets']
        for participantDmg in range(5, 10):
            teamTurretDmgList[1] += matchListInfo['matchDetailInfo']['participants'][participantDmg]['stats']['damageDealtToTurrets']

        try:
            turretDmgPart = round(matchListInfo['matchDetailInfo']['participants'][participantId]['stats']['damageDealtToTurrets'] / teamTurretDmgList[teamId], 2)
            matchListInfo.update({'turretDmgPart': "{0:.0%}".format(turretDmgPart)})
        except ZeroDivisionError:
            turretDmgPart = "No Turret Dmg dealt"
            matchListInfo.update({'turretDmgPart': turretDmgPart})

        # Gold Percentage in Team
        team1GoldEarned = 0
        team2GoldEarned = 0
        teamGoldEarnedList = [team1GoldEarned, team2GoldEarned]

        for participantGld in range(5):
            teamGoldEarnedList[0] += matchListInfo['matchDetailInfo']['participants'][participantGld]['stats']['goldEarned']
        for participantGld in range(5, 10):
            teamGoldEarnedList[1] += matchListInfo['matchDetailInfo']['participants'][participantGld]['stats']['goldEarned']

        try:
            goldEarnedPart = round(matchListInfo['matchDetailInfo']['participants'][participantId]['stats']['goldEarned'] / teamGoldEarnedList[teamId], 2)
            matchListInfo.update({'goldEarnedPart': "{0:.0%}".format(goldEarnedPart)})
        except ZeroDivisionError:
            goldEarnedPart = "No Gold Earned"
            matchListInfo.update({'goldEarnedPart': goldEarnedPart})


        # Get Forward Percentage
        # Create a List with all positions in one game
        positionList = []
        for triEntries in matchListInfo['matchTimeline']['frames']:
            for entry in range(1,11):
                if triEntries['participantFrames'][str(entry)]['participantId'] == participantIdValue:
                    try:
                        xy = [triEntries['participantFrames'][str(entry)]['position']['x'], triEntries['participantFrames'][str(entry)]['position']['y']]
                        positionList.append(xy)
                    except KeyError:
                        continue

        # Calc FWD
        fwdCounterList = []
        for coord in positionList:
            #formular to divide map in half
            if coord[1] >= -coord[0] + 14925:
                fwdCounterList.append(1)
            else:
                fwdCounterList.append(0)
        # depending on participant team
        if teamId == 0:
            fwd = "{0:.0%}".format(fwdCounterList.count(1) / len(fwdCounterList))
            matchListInfo.update({'fwd': fwd})
        else:
            fwd = "{0:.0%}".format(fwdCounterList.count(0) / len(fwdCounterList))
            matchListInfo.update({'fwd': fwd})

        # Calc FB Rate
        if matchListInfo['matchDetailInfo']['participants'][participantId]['stats']['firstBloodKill'] or matchListInfo['matchDetailInfo']['participants'][participantId]['stats']['firstBloodAssist'] == True:
            matchListInfo.update({'firstBlood': 'First Blood K/A'})
            fbList.append(True)

        # Calc FB Give Rate
        getFbGiveRate(matchListInfo['matchTimeline']['frames'], fbGiveList)

        # Get more matchDetail Information
        matchListInfo.update({'spell1Id': matchListInfo['matchDetailInfo']['participants'][participantId]['spell1Id'],
                              'spell2Id': matchListInfo['matchDetailInfo']['participants'][participantId]['spell2Id'],
                              'spell1Link': getSumSpellLink(sumSpells['data'].items(),matchListInfo['matchDetailInfo']['participants'][participantId]['spell1Id']),
                              'spell2Link': getSumSpellLink(sumSpells['data'].items(),matchListInfo['matchDetailInfo']['participants'][participantId]['spell2Id']),
                              'item0': matchListInfo['matchDetailInfo']['participants'][participantId]['stats']['item0'],
                              'item1': matchListInfo['matchDetailInfo']['participants'][participantId]['stats']['item1'],
                              'item2': matchListInfo['matchDetailInfo']['participants'][participantId]['stats']['item2'],
                              'item3': matchListInfo['matchDetailInfo']['participants'][participantId]['stats']['item3'],
                              'item4': matchListInfo['matchDetailInfo']['participants'][participantId]['stats']['item4'],
                              'item5': matchListInfo['matchDetailInfo']['participants'][participantId]['stats']['item5'],
                              'item6': matchListInfo['matchDetailInfo']['participants'][participantId]['stats']['item6'],
                              'kills': matchListInfo['matchDetailInfo']['participants'][participantId]['stats']['kills'],
                              'deaths': matchListInfo['matchDetailInfo']['participants'][participantId]['stats']['deaths'],
                              'assists': matchListInfo['matchDetailInfo']['participants'][participantId]['stats']['assists'],
                              'champLevel': matchListInfo['matchDetailInfo']['participants'][participantId]['stats']['champLevel'],
                              'visionScore': matchListInfo['matchDetailInfo']['participants'][participantId]['stats']['visionScore'],
                              'perkPrimaryStyle': matchListInfo['matchDetailInfo']['participants'][participantId]['stats']['perkPrimaryStyle'],
                              'perkSubStyle': matchListInfo['matchDetailInfo']['participants'][participantId]['stats']['perkSubStyle'],
                              'perk0': matchListInfo['matchDetailInfo']['participants'][participantId]['stats']['perk0'],
                              'keystoneLink': getRunesLink(runes,matchListInfo['matchDetailInfo']['participants'][participantId]['stats']['perkPrimaryStyle'],matchListInfo['matchDetailInfo']['participants'][participantId]['stats']['perk0']),
                              'keystone2Link': getSecRunesLink(runes, matchListInfo['matchDetailInfo']['participants'][participantId]['stats']['perkSubStyle']),

                              })

        # error handling in dict=========================================================================================================
        # Zero Division of KDA
        try:
            matchListInfo.update({'kda': round((matchListInfo['matchDetailInfo']['participants'][participantId]['stats']['kills'] + matchListInfo['matchDetailInfo']['participants'][participantId]['stats']['assists'])/matchListInfo['matchDetailInfo']['participants'][participantId]['stats']['deaths'],2)})
        except ZeroDivisionError:
            matchListInfo.update({'kda': "Perfect"})

        # emtpy item slots directed to grey placeholder if id= 0
        for itemslot in range(7):
            if matchListInfo['matchDetailInfo']['participants'][participantId]['stats']['item' + str(itemslot)] == 0:
                matchListInfo.update({str('item' + str(itemslot) + 'Link'): "https://opgg-static.akamaized.net/images/pattern/opacity.1.png"})
            else:
                matchListInfo.update({str('item' + str(itemslot) + 'Link'): getItemLink(items['data'].items(),matchListInfo['matchDetailInfo']['participants'][participantId]['stats']['item' + str(itemslot)]),})


        # Finally add all updates to a list
        matchList_data.append(matchListInfo)

        index += 1
        if index == limit:
            break

    #                                #
    # Stats involving multiple games #
    #                                #

    # Get SoloQ and flexQ last game played
    lastSoloQGame = 'Longer than 20 Games ago'
    lastFlexQGame = 'Longer than 20 games ago'
    for entry in matchList_data:
        if entry['queue'] == 420:
            lastSoloQGame = 'Last Played: ' + str(entry['lastGame']) + ' hours ago'
            break
    for entry in matchList_data:
        if entry['queue'] == 440:
            lastFlexQGame = 'Last Played: ' + str(entry['lastGame']) + ' hours ago'
            break

    # FB rate
    fbRate = "{0:.0%}".format(fbList.count(True) / len(matchList_data))

    # FB Give Rate
    fbGiveRate = "{0:.0%}".format(fbGiveList.count(True) / len(matchList_data))

    # Get summoner average data
    #DPM
    avgDPM = getAvgData(matchList_data, 'dpm')

    #Damage %
    avgDmgPart = getAvgData(matchList_data, 'dmgPart')

    #KP
    avgKP = getAvgData(matchList_data, 'killPart')

    #Gold%
    avgGoldPart = getAvgData(matchList_data, 'goldEarnedPart')



    # All Variables in one place
    context = {
        'responseSummonerData': responseSummonerData,
        'query':query,
        'matchList_data': matchList_data,
        'matchDetail_data': matchDetail_data,
        'responseMatchList': responseMatchList,
        'lastSoloQGame': lastSoloQGame,
        'lastFlexQGame': lastFlexQGame,
        'soloqWR': soloqWR,
        'flexqWR': flexqWR,
        'rangeTen': rangeTen,
        'fbRate': fbRate,
        'fbGiveRate': fbGiveRate,
        'avgDPM': avgDPM,
        'avgDmgPart': avgDmgPart,
        'avgKP': avgKP,
        'avgGoldPart': avgGoldPart,
    }

    if bool(responseRankedData)== True:
        context.update({'soloRankedData': soloRankedData,})
        context.update({'flexRankedData': flexRankedData, })


    return render(request, 'player/cheatsheet_index.html', context)

# Utility ############################################################

def search(request):
    template = 'search/search.html'

    query = request.GET.get('q', '')


    return render(request, template, { 'query': query})

# Webhook
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def update(request):
    if request.method == "POST":
        '''
        pass the path of the diectory where your project will be
        stored on PythonAnywhere in the git.Repo() as parameter.
        Here the name of my directory is "test.pythonanywhere.com"
        '''
        repo = git.Repo("goprogg.pythonanywhere.com/")
        origin = repo.remotes.origin

        origin.pull()

        return HttpResponse("Updated code on PythonAnywhere")
    else:
        return HttpResponse("Couldn't update the code on PythonAnywhere")

