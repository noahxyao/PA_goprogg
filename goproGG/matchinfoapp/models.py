# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class MatchlistV4(models.Model):
    primarykey = models.AutoField(primary_key=True)
    accountid = models.CharField(db_column='accountId', max_length=255, blank=True, null=True)  # Field name made lowercase.
    platformid = models.CharField(db_column='platformId', max_length=255, blank=True, null=True)  # Field name made lowercase.
    gameid = models.BigIntegerField(db_column='gameId', blank=True, null=True)  # Field name made lowercase.
    champion = models.IntegerField(blank=True, null=True)
    queue = models.IntegerField(blank=True, null=True)
    season = models.IntegerField(blank=True, null=True)
    timestamp = models.BigIntegerField(blank=True, null=True)
    role = models.CharField(max_length=255, blank=True, null=True)
    lane = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'MatchList_V4'


class MatchparticipantV4(models.Model):
    primarykey = models.AutoField(primary_key=True)
    gameid = models.BigIntegerField(db_column='gameId', blank=True, null=True)  # Field name made lowercase.
    platformid = models.CharField(db_column='platformId', max_length=255, blank=True, null=True)  # Field name made lowercase.
    gamecreation = models.BigIntegerField(db_column='gameCreation', blank=True, null=True)  # Field name made lowercase.
    gameduration = models.IntegerField(db_column='gameDuration', blank=True, null=True)  # Field name made lowercase.
    queueid = models.IntegerField(db_column='queueId', blank=True, null=True)  # Field name made lowercase.
    mapid = models.IntegerField(db_column='mapId', blank=True, null=True)  # Field name made lowercase.
    seasonid = models.IntegerField(db_column='seasonId', blank=True, null=True)  # Field name made lowercase.
    gameversion = models.CharField(db_column='gameVersion', max_length=255, blank=True, null=True)  # Field name made lowercase.
    gamemode = models.CharField(db_column='gameMode', max_length=255, blank=True, null=True)  # Field name made lowercase.
    gametype = models.CharField(db_column='gameType', max_length=255, blank=True, null=True)  # Field name made lowercase.
    teamid = models.IntegerField(db_column='teamId', blank=True, null=True)  # Field name made lowercase.
    participantid = models.IntegerField(db_column='participantId', blank=True, null=True)  # Field name made lowercase.
    accountid = models.CharField(db_column='accountId', max_length=255, blank=True, null=True)  # Field name made lowercase.
    summonername = models.CharField(db_column='summonerName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    summonerid = models.CharField(db_column='summonerId', max_length=255, blank=True, null=True)  # Field name made lowercase.
    matchhistoryuri = models.CharField(db_column='matchHistoryUri', max_length=255, blank=True, null=True)  # Field name made lowercase.
    championid = models.IntegerField(db_column='championId', blank=True, null=True)  # Field name made lowercase.
    spell1id = models.IntegerField(db_column='spell1Id', blank=True, null=True)  # Field name made lowercase.
    spell2id = models.IntegerField(db_column='spell2Id', blank=True, null=True)  # Field name made lowercase.
    role = models.CharField(max_length=255, blank=True, null=True)
    lane = models.CharField(max_length=255, blank=True, null=True)
    win = models.IntegerField(blank=True, null=True)
    item0 = models.IntegerField(blank=True, null=True)
    item1 = models.IntegerField(blank=True, null=True)
    item2 = models.IntegerField(blank=True, null=True)
    item3 = models.IntegerField(blank=True, null=True)
    item4 = models.IntegerField(blank=True, null=True)
    item5 = models.IntegerField(blank=True, null=True)
    item6 = models.IntegerField(blank=True, null=True)
    kills = models.IntegerField(blank=True, null=True)
    deaths = models.IntegerField(blank=True, null=True)
    assists = models.IntegerField(blank=True, null=True)
    largestkillingspree = models.IntegerField(db_column='largestKillingSpree', blank=True, null=True)  # Field name made lowercase.
    largestmultikill = models.IntegerField(db_column='largestMultiKill', blank=True, null=True)  # Field name made lowercase.
    killingsprees = models.IntegerField(db_column='killingSprees', blank=True, null=True)  # Field name made lowercase.
    longesttimespentliving = models.IntegerField(db_column='longestTimeSpentLiving', blank=True, null=True)  # Field name made lowercase.
    doublekills = models.IntegerField(db_column='doubleKills', blank=True, null=True)  # Field name made lowercase.
    triplekills = models.IntegerField(db_column='tripleKills', blank=True, null=True)  # Field name made lowercase.
    quadrakills = models.IntegerField(db_column='quadraKills', blank=True, null=True)  # Field name made lowercase.
    pentakills = models.IntegerField(db_column='pentaKills', blank=True, null=True)  # Field name made lowercase.
    unrealkills = models.IntegerField(db_column='unrealKills', blank=True, null=True)  # Field name made lowercase.
    totaldamagedealt = models.IntegerField(db_column='totalDamageDealt', blank=True, null=True)  # Field name made lowercase.
    magicdamagedealt = models.IntegerField(db_column='magicDamageDealt', blank=True, null=True)  # Field name made lowercase.
    physicaldamagedealt = models.IntegerField(db_column='physicalDamageDealt', blank=True, null=True)  # Field name made lowercase.
    truedamagedealt = models.IntegerField(db_column='trueDamageDealt', blank=True, null=True)  # Field name made lowercase.
    largestcriticalstrike = models.IntegerField(db_column='largestCriticalStrike', blank=True, null=True)  # Field name made lowercase.
    totaldamagedealttochampions = models.IntegerField(db_column='totalDamageDealtToChampions', blank=True, null=True)  # Field name made lowercase.
    magicdamagedealttochampions = models.IntegerField(db_column='magicDamageDealtToChampions', blank=True, null=True)  # Field name made lowercase.
    physicaldamagedealttochampions = models.IntegerField(db_column='physicalDamageDealtToChampions', blank=True, null=True)  # Field name made lowercase.
    truedamagedealttochampions = models.IntegerField(db_column='trueDamageDealtToChampions', blank=True, null=True)  # Field name made lowercase.
    totalheal = models.IntegerField(db_column='totalHeal', blank=True, null=True)  # Field name made lowercase.
    totalunitshealed = models.IntegerField(db_column='totalUnitsHealed', blank=True, null=True)  # Field name made lowercase.
    damageselfmitigated = models.IntegerField(db_column='damageSelfMitigated', blank=True, null=True)  # Field name made lowercase.
    damagedealttoobjectives = models.IntegerField(db_column='damageDealtToObjectives', blank=True, null=True)  # Field name made lowercase.
    damagedealttoturrets = models.IntegerField(db_column='damageDealtToTurrets', blank=True, null=True)  # Field name made lowercase.
    visionscore = models.IntegerField(db_column='visionScore', blank=True, null=True)  # Field name made lowercase.
    timeccingothers = models.IntegerField(db_column='timeCCingOthers', blank=True, null=True)  # Field name made lowercase.
    totaldamagetaken = models.IntegerField(db_column='totalDamageTaken', blank=True, null=True)  # Field name made lowercase.
    magicaldamagetaken = models.IntegerField(db_column='magicalDamageTaken', blank=True, null=True)  # Field name made lowercase.
    physicaldamagetaken = models.IntegerField(db_column='physicalDamageTaken', blank=True, null=True)  # Field name made lowercase.
    truedamagetaken = models.IntegerField(db_column='trueDamageTaken', blank=True, null=True)  # Field name made lowercase.
    goldearned = models.IntegerField(db_column='goldEarned', blank=True, null=True)  # Field name made lowercase.
    goldspent = models.IntegerField(db_column='goldSpent', blank=True, null=True)  # Field name made lowercase.
    turretkills = models.IntegerField(db_column='turretKills', blank=True, null=True)  # Field name made lowercase.
    inhibitorkills = models.IntegerField(db_column='inhibitorKills', blank=True, null=True)  # Field name made lowercase.
    totalminionskilled = models.IntegerField(db_column='totalMinionsKilled', blank=True, null=True)  # Field name made lowercase.
    neutralminionskilled = models.IntegerField(db_column='neutralMinionsKilled', blank=True, null=True)  # Field name made lowercase.
    neutralminionskilledteamjungle = models.IntegerField(db_column='neutralMinionsKilledTeamJungle', blank=True, null=True)  # Field name made lowercase.
    neutralminionskilledenemyjungle = models.IntegerField(db_column='neutralMinionsKilledEnemyJungle', blank=True, null=True)  # Field name made lowercase.
    totaltimecrowdcontroldealt = models.IntegerField(db_column='totalTimeCrowdControlDealt', blank=True, null=True)  # Field name made lowercase.
    champlevel = models.IntegerField(db_column='champLevel', blank=True, null=True)  # Field name made lowercase.
    visionwardsboughtingame = models.IntegerField(db_column='visionWardsBoughtInGame', blank=True, null=True)  # Field name made lowercase.
    sightwardsboughtingame = models.IntegerField(db_column='sightWardsBoughtInGame', blank=True, null=True)  # Field name made lowercase.
    wardsplaced = models.IntegerField(db_column='wardsPlaced', blank=True, null=True)  # Field name made lowercase.
    wardskilled = models.IntegerField(db_column='wardsKilled', blank=True, null=True)  # Field name made lowercase.
    firstbloodkill = models.IntegerField(db_column='firstBloodKill', blank=True, null=True)  # Field name made lowercase.
    firstbloodassist = models.IntegerField(db_column='firstBloodAssist', blank=True, null=True)  # Field name made lowercase.
    firsttowerkill = models.IntegerField(db_column='firstTowerKill', blank=True, null=True)  # Field name made lowercase.
    firsttowerassist = models.IntegerField(db_column='firstTowerAssist', blank=True, null=True)  # Field name made lowercase.
    firstinhibitorkill = models.IntegerField(db_column='firstInhibitorKill', blank=True, null=True)  # Field name made lowercase.
    firstinhibitorassist = models.IntegerField(db_column='firstInhibitorAssist', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'MatchParticipant_V4'


class MatchteamV4(models.Model):
    primarykey = models.AutoField(primary_key=True)
    gameid = models.BigIntegerField(db_column='gameId', blank=True, null=True)  # Field name made lowercase.
    platformid = models.CharField(db_column='platformId', max_length=255, blank=True, null=True)  # Field name made lowercase.
    gamecreation = models.BigIntegerField(db_column='gameCreation', blank=True, null=True)  # Field name made lowercase.
    gameduration = models.IntegerField(db_column='gameDuration', blank=True, null=True)  # Field name made lowercase.
    queueid = models.IntegerField(db_column='queueId', blank=True, null=True)  # Field name made lowercase.
    mapid = models.IntegerField(db_column='mapId', blank=True, null=True)  # Field name made lowercase.
    seasonid = models.IntegerField(db_column='seasonId', blank=True, null=True)  # Field name made lowercase.
    gameversion = models.CharField(db_column='gameVersion', max_length=255, blank=True, null=True)  # Field name made lowercase.
    gamemode = models.CharField(db_column='gameMode', max_length=255, blank=True, null=True)  # Field name made lowercase.
    gametype = models.CharField(db_column='gameType', max_length=255, blank=True, null=True)  # Field name made lowercase.
    teamid = models.IntegerField(db_column='teamId', blank=True, null=True)  # Field name made lowercase.
    win = models.CharField(max_length=255, blank=True, null=True)
    firstblood = models.IntegerField(db_column='firstBlood', blank=True, null=True)  # Field name made lowercase.
    firsttower = models.IntegerField(db_column='firstTower', blank=True, null=True)  # Field name made lowercase.
    firstinhibitor = models.IntegerField(db_column='firstInhibitor', blank=True, null=True)  # Field name made lowercase.
    firstbaron = models.IntegerField(db_column='firstBaron', blank=True, null=True)  # Field name made lowercase.
    firstdragon = models.IntegerField(db_column='firstDragon', blank=True, null=True)  # Field name made lowercase.
    firstriftherald = models.IntegerField(db_column='firstRiftHerald', blank=True, null=True)  # Field name made lowercase.
    towerkills = models.IntegerField(db_column='towerKills', blank=True, null=True)  # Field name made lowercase.
    inhibitorkills = models.IntegerField(db_column='inhibitorKills', blank=True, null=True)  # Field name made lowercase.
    baronkills = models.IntegerField(db_column='baronKills', blank=True, null=True)  # Field name made lowercase.
    dragonkills = models.IntegerField(db_column='dragonKills', blank=True, null=True)  # Field name made lowercase.
    vilemawkills = models.IntegerField(db_column='vilemawKills', blank=True, null=True)  # Field name made lowercase.
    riftheraldkills = models.IntegerField(db_column='riftHeraldKills', blank=True, null=True)  # Field name made lowercase.
    dominionvictoryscore = models.IntegerField(db_column='dominionVictoryScore', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'MatchTeam_V4'


class SummonerV4(models.Model):
    primarykey = models.AutoField(primary_key=True)
    id = models.CharField(max_length=255, blank=True, null=True)
    accountid = models.CharField(db_column='accountId', max_length=255, blank=True, null=True)  # Field name made lowercase.
    puuid = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    profileiconid = models.IntegerField(db_column='profileIconId', blank=True, null=True)  # Field name made lowercase.
    revisiondate = models.BigIntegerField(db_column='revisionDate', blank=True, null=True)  # Field name made lowercase.
    summonerlevel = models.IntegerField(db_column='summonerLevel', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Summoner_V4'