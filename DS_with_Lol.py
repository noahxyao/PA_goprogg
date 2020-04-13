import mysql.connector as mariadb
import requests
from statistics import mean
import numpy





connection = mariadb.connect(user='root', password='123321Almitimo', database='RiotGames')

cursor = connection.cursor()

summonerName = input("Which Summoner? ")

getAllPlayerGames = """SELECT * FROM MatchParticipant_V4 WHERE summonerName = """ + "'" +str(summonerName) + "'" + """ GROUP BY gameId
					ORDER BY `MatchParticipant_V4`.`gameCreation`  DESC"""



cursor.execute(getAllPlayerGames)

AllPlayerGames = cursor.fetchall()

print("Total number of games in Database is: ", cursor.rowcount)

kills = []
deaths = []
assists = []
kda = []

for row in AllPlayerGames:
	# print("kills = ", row[30])
	kills.append(row[30])

	# print("deaths = ", row[31])
	deaths.append(row[31])

	# print("assists = ", row[32], "\n") 
	assists.append(row[32])

	try:
		kda.append((row[30] + row[32]) / row[31])
	except ZeroDivisionError:
		continue


meanKda = numpy.mean(kda)
sumKda = numpy.sum(kda)

print("Accumulated Stats of past", cursor.rowcount, "Games: ")
print("kills = ", numpy.sum(kills))
print("deaths = ", numpy.sum(deaths))
print("assists = ", numpy.sum(assists))



print("Kda of last Game = ", numpy.mean(kda[0]))
print("Kda of past", cursor.rowcount, "Games = ", meanKda)


if connection.is_connected():
	connection.close()
	cursor.close()
	print("SQL connection is closed")