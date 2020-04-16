import mysql.connector as mariadb
import rg_api_key
import requests
import json
import asyncio


connection = mariadb.connect(user='root', password='123321Almitimo', database='RiotGames')

cursor = connection.cursor()

#Test away ======================================

getDBsummonerName = """SELECT name FROM Summoner_V4"""

cursor.execute(getDBsummonerName)

sumName = cursor.fetchall()

nameList = []
for name in sumName:
	nameList.append(name[0].replace(" ","").casefold())
print(nameList)


x = input("name").replace(" ","").casefold()

if x in nameList:
	print("x is in List")
else:
	print("new name!")