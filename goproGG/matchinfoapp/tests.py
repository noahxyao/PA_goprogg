import requests
import json
import re

def capital_words_spaces(str1):
    return re.sub(r"(\w)([A-Z])", r"\1 \2", str1)
  

def getChamps():
    champs = requests.get("http://ddragon.leagueoflegends.com/cdn/10.8.1/data/en_US/champion.json")
    return champs.json()

champions = getChamps()
print(champions['data']['Aatrox']['key'])

x = str(64)

def getChampName(champList, currentCheck):
    for name, champEntry in champList:
        if currentCheck == champEntry['key']:
            champName = name
            return capital_words_spaces(champName)
            break

getChampName(x, 64)