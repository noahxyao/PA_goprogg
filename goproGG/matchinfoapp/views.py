from django.shortcuts import render
import requests

def requestSummonerData(region, summonerName, APIKey):

    #Here is how I make my URL.  There are many ways to create these.
    
    URL = "https://" + region + ".api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summonerName + "?api_key=" + APIKey
    #print(URL)
    #requests.get is a function given to us my our import "requests". It basically goes to the URL we made and gives us back a JSON.
    response = requests.get(URL)
    #Here I return the JSON we just got.
    return response.json()

def requestRankedData(region, ID, APIKey):
    URL = "https://" + region + ".api.riotgames.com/lol/league/v4/entries/by-summoner/" + ID + "?api_key=" + APIKey
    #print(URL)
    response = requests.get(URL)
    return response.json()


region = "EUW1"
summonerName = 'minras'
APIKey = 'RGAPI-d2338c5a-8795-4ef8-8208-d50c72f14b54'

#I send these three pieces off to my requestData function which will create the URL and give me back a JSON that has the ID for that specific summoner.
#Once again, what requestData returns is a JSON.
responseJSON  = requestSummonerData(region, summonerName, APIKey)

#print (responseJSON)

ID = responseJSON['id']
ID = str(ID)
#print (ID)
responseJSON2 = requestRankedData(region, ID, APIKey)


def index(request):
	
	return render(request, 'ranked/index.html', {'data':responseJSON2})