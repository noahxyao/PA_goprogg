from django.shortcuts import render
import requests
from datetime import datetime
import time
from .models import SummonerV4, MatchlistV4, MatchparticipantV4, MatchteamV4
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

# DB Functions
def requestMatchListDB(accountId, limit):
    queryset = MatchlistV4.objects.filter(accountid=accountId).order_by('-timestamp')[0:limit]
    return queryset

def requestMatchTeamDB(matchId):
    queryset = MatchteamV4.objects.filter(gameid=matchId).order_by('teamid')#.distinct('teamid')
    return queryset

def requestMatchInfoDB(matchId):
    queryset = MatchparticipantV4.objects.filter(gameid=matchId).order_by('participantid').values()
    return queryset

def requestMatchTimelineDB(matchId):
    queryset = MatchlistV4.objects.filter(accountid=accountId).order_by('-timestamp')[0:limit]
    return queryset

def getDistinct(query, participantid, value):
    for i in query:
        if i['participantid'] == participantid:
            return i[value]

region = "EUW1"
APIKey = 'RGAPI-9d45440f-231b-49dc-b601-1dd545c3bb99'



def player(request):
    # Define some global variables to use later
    global soloRankedData, flexRankedData, soloRankedContext, flexRankedContext, participantIdValue
    # User Input
    query = request.GET.get('q', '')
    summonerName = query

    # manually enter sumName without search box
    # sumName = SummonerV4.objects.filter(name__icontains=query)[0].name

    # Get Real Time User data from Riot API, get all champ data from DDragon
    responseSummonerData = requestSummonerData(region, summonerName, APIKey)
    ID = responseSummonerData['id']
    accountId = responseSummonerData['accountId']
    responseRankedData = requestRankedData(region, ID, APIKey)

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
    # Get data from DB and CDN
    # responseMatchList = requestMatchList(region, accountId, APIKey)
    responseMatchList = requestMatchListDB(accountId, limit)
    # DDragon
    champions = getChamps()
    items = getItems()
    sumSpells = getSumSpells()
    runes = getRunes()

    # Declare variables to be used outside the individual matches
    matchList_data = []
    matchDetail_data = []
    fbList = []
    fbGiveList = []
    rangeTen = [1,2,3,4,5,6,7,8,9,10]

    # Start populating my dataset ###################################################################################################
    for i in range(len(responseMatchList)):
        matchListInfo = {
            'gameId': responseMatchList[i].gameid,
            'champion': responseMatchList[i].champion,
            'championName': getChampName(champions['data'].items(), responseMatchList[i].champion),
            'championLink': getChampLink(champLinks.items(), responseMatchList[i].champion),
            'queue': responseMatchList[i].queue,
            'queueType': queueType[str(responseMatchList[i].queue)],
            'season': responseMatchList[i].season,
            'timestamp': responseMatchList[i].timestamp,
            'lastGame': requestLastGamePlayed(responseMatchList[i].timestamp),
            'role':responseMatchList[i].role,
            'lane': responseMatchList[i].lane,
            # API response for match Details
            # 'matchTeamInfo': requestMatchTeamDB(responseMatchList[i].gameid),
            'matchDetailInfo': requestMatchInfoDB(responseMatchList[i].gameid),
            # 'matchTimeline': requestMatchTimelineDB(responseMatchList[i].gameid),
        }

        # Remove duplicates from matchDetailInfo =================================
        # Create dict in dict
        matchDetailInfo_Dict = {}
        keys = range(len(matchListInfo['matchDetailInfo']))
        for key in keys:
            matchDetailInfo_Dict[str(key)] = None

        partCounter = 0
        for participant in matchListInfo['matchDetailInfo']:
            matchDetailInfo2 = {
                'gameid': participant['gameid'],
                'platformid': participant['platformid'],
                'gamecreation': participant['gamecreation'],
                'gameduration': participant['gameduration'],
                'queueid': participant['queueid'],
                'mapid': participant['mapid'],
                'seasonid': participant['seasonid'],
                'gameversion': participant['gameversion'],
                'gamemode': participant['gamemode'],
                'gametype': participant['gametype'],
                'teamid': participant['teamid'],
                'participantid': participant['participantid'],
                'accountid': participant['accountid'],
                'summonername': participant['summonername'],
                'summonerid': participant['summonerid'],
                'matchhistoryuri': participant['matchhistoryuri'],
                'championid': participant['championid'],
                'spell1id': participant['spell1id'],
                'spell2id': participant['spell2id'],
                'role': participant['role'],
                'lane': participant['lane'],
                'win': participant['win'],
                'item0': participant['item0'],
                'item1': participant['item1'],
                'item2': participant['item2'],
                'item3': participant['item3'],
                'item4': participant['item4'],
                'item5': participant['item5'],
                'item6': participant['item6'],
                'kills': participant['kills'],
                'deaths': participant['deaths'],
                'assists': participant['assists'],
                'largestkillingspree': participant['largestkillingspree'],
                'largestmultikill': participant['largestmultikill'],
                'killingsprees': participant['killingsprees'],
                'longesttimespentliving': participant['longesttimespentliving'],
                'doublekills': participant['doublekills'],
                'triplekills': participant['triplekills'],
                'quadrakills': participant['quadrakills'],
                'pentakills': participant['pentakills'],
                'unrealkills': participant['unrealkills'],
                'totaldamagedealt': participant['totaldamagedealt'],
                'magicdamagedealt': participant['magicdamagedealt'],
                'physicaldamagedealt': participant['physicaldamagedealt'],
                'truedamagedealt': participant['truedamagedealt'],
                'largestcriticalstrike': participant['largestcriticalstrike'],
                'totaldamagedealttochampions': participant['totaldamagedealttochampions'],
                'magicdamagedealttochampions': participant['magicdamagedealttochampions'],
                'physicaldamagedealttochampions': participant['physicaldamagedealttochampions'],
                'truedamagedealttochampions': participant['truedamagedealttochampions'],
                'totalheal': participant['totalheal'],
                'totalunitshealed': participant['totalunitshealed'],
                'damageselfmitigated': participant['damageselfmitigated'],
                'damagedealttoobjectives': participant['damagedealttoobjectives'],
                'damagedealttoturrets': participant['damagedealttoturrets'],
                'visionscore': participant['visionscore'],
                'timeccingothers': participant['timeccingothers'],
                'totaldamagetaken': participant['totaldamagetaken'],
                'magicaldamagetaken': participant['magicaldamagetaken'],
                'physicaldamagetaken': participant['physicaldamagetaken'],
                'truedamagetaken': participant['truedamagetaken'],
                'goldearned': participant['goldearned'],
                'goldspent': participant['goldspent'],
                'turretkills': participant['turretkills'],
                'inhibitorkills': participant['inhibitorkills'],
                'totalminionskilled': participant['totalminionskilled'],
                'neutralminionskilled': participant['neutralminionskilled'],
                'neutralminionskilledteamjungle': participant['neutralminionskilledteamjungle'],
                'neutralminionskilledenemyjungle': participant['neutralminionskilledenemyjungle'],
                'totaltimecrowdcontroldealt': participant['totaltimecrowdcontroldealt'],
                'champlevel': participant['champlevel'],
                'visionwardsboughtingame': participant['visionwardsboughtingame'],
                'sightwardsboughtingame': participant['sightwardsboughtingame'],
                'wardsplaced': participant['wardsplaced'],
                'wardskilled': participant['wardskilled'],
                'firstbloodkill': participant['firstbloodkill'],
                'firstbloodassist': participant['firstbloodassist'],
                'firsttowerkill': participant['firsttowerkill'],
                'firsttowerassist': participant['firsttowerassist'],
                'firstinhibitorkill': participant['firstinhibitorkill'],
                'firstinhibitorassist': participant['firstinhibitorassist'],
                'perk0': participant['perk0'],
                'perk1': participant['perk1'],
                'perk2': participant['perk2'],
                'perk3': participant['perk3'],
                'perk4': participant['perk4'],
                'perk5': participant['perk5'],
                'perkprimarystyle': participant['perkprimarystyle'],
                'perksubstyle': participant['perksubstyle'],
            }
            matchDetailInfo_Dict.update({str(partCounter): matchDetailInfo2})
            partCounter += 1
        # Filter out duplicate db rows
        matchDetailInfoDistinct = {}
        for key, value in matchDetailInfo_Dict.items():
            if value not in matchDetailInfoDistinct.values():
                matchDetailInfoDistinct[key] = value
        # Clean dict names to participant numbers
        keyList = [i + 1 for i in range(10)]
        matchDetailInfoDistinctClean = dict(zip(keyList, list(matchDetailInfoDistinct.values())))

        matchListInfo.update({'matchDetailInfox': matchDetailInfoDistinctClean})
        # Dataset Details done ########################################################################################################

        # Get champ pictures for all participants of same game
        for participant in range(1,11):
            matchListInfo.update({
                "champLink_" + str(participant): getChampLink(champLinks.items(),matchListInfo['matchDetailInfox'][participant]['championid']),
            }
        )

        # Get match information of current summoner
        for i in matchListInfo['matchDetailInfox']:
            if matchListInfo['matchDetailInfox'][i]['summonername'] == responseSummonerData['name']:
                participantId = matchListInfo['matchDetailInfox'][i]['participantid']
                teamId = matchListInfo['matchDetailInfox'][i]['teamid']
                # Get match result for summoner's participantId
                if matchListInfo['matchDetailInfox'][i]['win'] == True:
                    matchListInfo.update({"result": 'Victory'})
                else:
                    matchListInfo.update({"result": 'Defeat'})

                # Add Multikills
                if matchListInfo['matchDetailInfox'][i]['largestmultikill'] > 1:
                    killDict = {'2': 'Doublekill',
                                '3': 'Triplekill',
                                '4': 'Quadrakill',
                                '5': 'Pentakill',
                                }
                    matchListInfo.update({'largestMultiKill': killDict[str(matchListInfo['matchDetailInfox'][i]['largestmultikill'])]})

                # Add total CS
                totalCS = matchListInfo['matchDetailInfox'][i]['totalminionskilled'] + matchListInfo['matchDetailInfox'][i]['neutralminionskilled']
                matchListInfo.update({'totalCS': totalCS})

                # Add Game Duration and duration related variables
                gameDuration = matchListInfo['matchDetailInfox'][i]['gameduration']
                gameDurationMin = time.strftime('%M', time.gmtime(gameDuration))
                gameDurationSec = time.strftime('%S', time.gmtime(gameDuration))
                # cs per min
                cspMin = round(totalCS/(int(gameDurationMin) + int(gameDurationSec)/60),2)
                # dmg per min
                dpm = round(matchListInfo['matchDetailInfox'][i]['totaldamagedealttochampions'] / (int(gameDurationMin) + int(gameDurationSec)/60),2)

                matchListInfo.update({'gameDurationMin': gameDurationMin,
                                      'gameDurationSec': gameDurationSec,
                                      'cspMin': cspMin,
                                      'dpm': dpm,
                                      })

                break

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

        for participant in range(1, 6):
            teamKdaList[0][0] += matchListInfo['matchDetailInfox'][participant]['kills']
            teamKdaList[0][1] += matchListInfo['matchDetailInfox'][participant]['deaths']
            teamKdaList[0][2] += matchListInfo['matchDetailInfox'][participant]['assists']
        for participant in range(6, 11):
            teamKdaList[1][0] += matchListInfo['matchDetailInfox'][participant]['kills']
            teamKdaList[1][1] += matchListInfo['matchDetailInfox'][participant]['deaths']
            teamKdaList[1][2] += matchListInfo['matchDetailInfox'][participant]['assists']

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
        teamKillsDict = {100: teamKdaList[0][0], 200: teamKdaList[1][0]}

        try:
            killPart = round((matchListInfo['matchDetailInfox'][participantId]['kills'] + matchListInfo['matchDetailInfox'][participantId]['assists'])/teamKillsDict[teamId], 2)
            matchListInfo.update({'killPart': "{0:.0%}".format(killPart)})
        except ZeroDivisionError:
            killPart = "No Kills"
            matchListInfo.update({'killPart': killPart})

        # Dmg Participation: Dmg Dealt to Champions
        team1DamageChamps = 0
        team2DamageChamps = 0
        teamDmgChampsDict = {100: team1DamageChamps, 200: team2DamageChamps}

        for participantDmg in range(1,6):
            teamDmgChampsDict[100] += matchListInfo['matchDetailInfox'][participantDmg]['totaldamagedealttochampions']
        for participantDmg in range(6,11):
            teamDmgChampsDict[200] += matchListInfo['matchDetailInfox'][participantDmg]['totaldamagedealttochampions']

        try:
            dmgPart = round(matchListInfo['matchDetailInfox'][participantId]['totaldamagedealttochampions'] / teamDmgChampsDict[teamId],2)
            matchListInfo.update({'dmgPart': "{0:.0%}".format(dmgPart)})
        except ZeroDivisionError:
            dmgPart = "No Dmg dealt"
            matchListInfo.update({'dmgPart': dmgPart})


        # Dmg Dealt to Turret Percentage in Team
        team1DamageTurrets = 0
        team2DamageTurrets = 0
        teamTurretDmgDict = {100: team1DamageTurrets, 200: team2DamageTurrets}

        for participantDmg in range(1,6):
            teamTurretDmgDict[100] += matchListInfo['matchDetailInfox'][participantDmg]['damagedealttoturrets']
        for participantDmg in range(6, 11):
            teamTurretDmgDict[200] += matchListInfo['matchDetailInfox'][participantDmg]['damagedealttoturrets']

        try:
            turretDmgPart = round(matchListInfo['matchDetailInfox'][participantId]['damagedealttoturrets'] / teamTurretDmgDict[teamId], 2)
            matchListInfo.update({'turretDmgPart': "{0:.0%}".format(turretDmgPart)})
        except ZeroDivisionError:
            turretDmgPart = "No Turret Dmg dealt"
            matchListInfo.update({'turretDmgPart': turretDmgPart})

        # Gold Percentage in Team
        team1GoldEarned = 0
        team2GoldEarned = 0
        teamGoldEarnedDict = {100: team1GoldEarned, 200: team2GoldEarned}

        for participantGld in range(1,6):
            teamGoldEarnedDict[100] += matchListInfo['matchDetailInfox'][participantGld]['goldearned']
        for participantGld in range(6, 11):
            teamGoldEarnedDict[200] += matchListInfo['matchDetailInfox'][participantGld]['goldearned']

        try:
            goldEarnedPart = round(matchListInfo['matchDetailInfox'][participantId]['goldearned'] / teamGoldEarnedDict[teamId], 2)
            matchListInfo.update({'goldEarnedPart': "{0:.0%}".format(goldEarnedPart)})
        except ZeroDivisionError:
            goldEarnedPart = "No Gold Earned"
            matchListInfo.update({'goldEarnedPart': goldEarnedPart})

    #
    #     # Get Forward Percentage
    #     # Create a List with all positions in one game
    #     positionList = []
    #     for triEntries in matchListInfo['matchTimeline']['frames']:
    #         for entry in range(1,11):
    #             if triEntries['participantFrames'][str(entry)]['participantId'] == participantIdValue:
    #                 try:
    #                     xy = [triEntries['participantFrames'][str(entry)]['position']['x'], triEntries['participantFrames'][str(entry)]['position']['y']]
    #                     positionList.append(xy)
    #                 except KeyError:
    #                     continue
    #
    #     # Calc FWD
    #     fwdCounterList = []
    #     for coord in positionList:
    #         #formular to divide map in half
    #         if coord[1] >= -coord[0] + 14925:
    #             fwdCounterList.append(1)
    #         else:
    #             fwdCounterList.append(0)
    #     # depending on participant team
    #     if teamId == 0:
    #         fwd = "{0:.0%}".format(fwdCounterList.count(1) / len(fwdCounterList))
    #         matchListInfo.update({'fwd': fwd})
    #     else:
    #         fwd = "{0:.0%}".format(fwdCounterList.count(0) / len(fwdCounterList))
    #         matchListInfo.update({'fwd': fwd})
    #
    #     # Calc FB Rate
    #     if matchListInfo['matchDetailInfo']['participants'][participantId]['stats']['firstBloodKill'] or matchListInfo['matchDetailInfo']['participants'][participantId]['stats']['firstBloodAssist'] == True:
    #         matchListInfo.update({'firstBlood': 'First Blood K/A'})
    #         fbList.append(True)
    #
    #     # Calc FB Give Rate
    #     getFbGiveRate(matchListInfo['matchTimeline']['frames'], fbGiveList)
    #
        # Get more matchDetail Information
        matchListInfo.update({'spell1Id': matchListInfo['matchDetailInfox'][participantId]['spell1id'],
                              'spell2Id': matchListInfo['matchDetailInfox'][participantId]['spell2id'],
                              'spell1Link': getSumSpellLink(sumSpells['data'].items(),matchListInfo['matchDetailInfox'][participantId]['spell1id']),
                              'spell2Link': getSumSpellLink(sumSpells['data'].items(),matchListInfo['matchDetailInfox'][participantId]['spell2id']),
                              'item0': matchListInfo['matchDetailInfox'][participantId]['item0'],
                              'item1': matchListInfo['matchDetailInfox'][participantId]['item1'],
                              'item2': matchListInfo['matchDetailInfox'][participantId]['item2'],
                              'item3': matchListInfo['matchDetailInfox'][participantId]['item3'],
                              'item4': matchListInfo['matchDetailInfox'][participantId]['item4'],
                              'item5': matchListInfo['matchDetailInfox'][participantId]['item5'],
                              'item6': matchListInfo['matchDetailInfox'][participantId]['item6'],
                              'kills': matchListInfo['matchDetailInfox'][participantId]['kills'],
                              'deaths': matchListInfo['matchDetailInfox'][participantId]['deaths'],
                              'assists': matchListInfo['matchDetailInfox'][participantId]['assists'],
                              'champLevel': matchListInfo['matchDetailInfox'][participantId]['champlevel'],
                              'visionScore': matchListInfo['matchDetailInfox'][participantId]['visionscore'],
                              'perkPrimaryStyle': matchListInfo['matchDetailInfox'][participantId]['perkprimarystyle'],
                              'perkSubStyle': matchListInfo['matchDetailInfox'][participantId]['perksubstyle'],
                              'perk0': matchListInfo['matchDetailInfox'][participantId]['perk0'],
                              'keystoneLink': getRunesLink(runes,matchListInfo['matchDetailInfox'][participantId]['perkprimarystyle'],matchListInfo['matchDetailInfox'][participantId]['perk0']),
                              'keystone2Link': getSecRunesLink(runes, matchListInfo['matchDetailInfox'][participantId]['perksubstyle']),

                              })

        # error handling in dict=========================================================================================================
        # Zero Division of KDA
        try:
            matchListInfo.update({'kda': round((matchListInfo['matchDetailInfox'][participantId]['kills'] + matchListInfo['matchDetailInfox'][participantId]['assists'])/matchListInfo['matchDetailInfox'][participantId]['deaths'],2)})
        except ZeroDivisionError:
            matchListInfo.update({'kda': "Perfect"})

        # emtpy item slots directed to grey placeholder if id= 0
        for itemslot in range(7):
            if matchListInfo['matchDetailInfox'][participantId]['item' + str(itemslot)] == 0:
                matchListInfo.update({str('item' + str(itemslot) + 'Link'): "https://opgg-static.akamaized.net/images/pattern/opacity.1.png"})
            else:
                matchListInfo.update({str('item' + str(itemslot) + 'Link'): getItemLink(items['data'].items(),matchListInfo['matchDetailInfox'][participantId]['item' + str(itemslot)]),})


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

    # # FB rate
    # fbRate = "{0:.0%}".format(fbList.count(True) / len(matchList_data))
    #
    # # FB Give Rate
    # fbGiveRate = "{0:.0%}".format(fbGiveList.count(True) / len(matchList_data))

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
        # 'matchDetail_data': matchDetail_data,
        'responseMatchList': responseMatchList,
        'lastSoloQGame': lastSoloQGame,
        'lastFlexQGame': lastFlexQGame,
        'soloqWR': soloqWR,
        'flexqWR': flexqWR,
        # 'rangeTen': rangeTen,
        # 'fbRate': fbRate,
        # 'fbGiveRate': fbGiveRate,
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


@csrf_exempt
def update(request):
    if request.method == "POST":
        '''
        pass the path of the diectory where your project will be
        stored on PythonAnywhere in the git.Repo() as parameter.
        Here the name of my directory is "test.pythonanywhere.com"
        '''
        repo = git.Repo("/home/goprogg/PA_goprogg/")
        origin = repo.remotes.origin

        origin.pull()

        return HttpResponse("Updated code on PythonAnywhere")
    else:
        return HttpResponse("Couldn't update the code on PythonAnywhere")



