import mysql.connector as mariadb
import requests
from statistics import mean
import numpy
import rg_api_key

#Standard DB Stuff
connection = mariadb.connect(user='root', password='123321Almitimo', database='RiotGames')

cursor = connection.cursor()

#query the DB for existing summonerName entry and save the table
getDBsummonerName = """SELECT name FROM Summoner_V4"""

cursor.execute(getDBsummonerName)

dbSumName = cursor.fetchall()

#Edit list of names so they can be matched easier with name input
dbNameList = []
for entry in dbSumName:
    dbNameList.append(entry[0].replace(" ","").casefold())


summonerName = input('Which Summoner? ').replace(" ","").casefold()

#
if summonerName in dbNameList:

    #query for the match data of this summoner
    getDBMatchData = """SELECT win, championId FROM MatchParticipant_V4 
        WHERE summonerName = """ + "'" + summonerName + "'" + """ GROUP BY gameId  
        ORDER BY gameCreation DESC"""

    #Create list of champion played in the counted matches
    champion = []
    for i in range(51):
        champion.append(responseJSON3['matches'][i]['champion'])


    #Put Match result into a list
    resultList = []
    kdaList = []
    m = 0
    for k in matchIdList:
        responseJSON4 = requestMatchInfo(region, str(k), APIKey)

        #find the participant through champion picked in match data
        for l in range(len(responseJSON4['participants'])):
            if responseJSON4['participants'][l]['championId'] != champion[m]:
                continue
                
            else:
                resultList.append(responseJSON4['participants'][l]['stats']['win'])
                m += 1


                
        #kdaList.append(responseJSON4['participants'][]['win'])
        
    #print(resultList)

    #Count Losses
    loss = 0
    win = 0
    for n in resultList:
        if n == True:
            win += 1
        else:
            loss +=1


    print('Number of Wins: ' + str(win) + '\nNumber of Losses: ' + str(loss) )


#This starts my program!
if __name__ == "__main__":
    main()

