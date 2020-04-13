#This tutorial was built by me, Farzain! You can ask me questions or troll me on Twitter (@farzatv)

#First we need to import requests. Installing this is a bit tricky. I included a step by step process on how to get requests in readme.txt which is included in the file along with this program.
import requests
import rg_api_key

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

def requestMatchList(region, accountID, APIKey):
    URL = "https://" + region + ".api.riotgames.com/lol/match/v4/matchlists/by-account/" + accountID + "?api_key=" + APIKey

    response = requests.get(URL)
    return response.json()

def getMatchId(responseJSON3, matchNumber):
    
    return responseJSON3['matches'][matchNumber]['gameId']

def requestMatchInfo(region, matchId, APIKey):
    URL = "https://" + region + ".api.riotgames.com/lol/match/v4/matches/" + matchId + "?api_key=" + APIKey

    response = requests.get(URL)
    return response.json()
    

def main():
    #print ("\nWhat up homie. Enter your region to get started")
    #print ("Type in one of the following regions or else the program wont work correctly:\n")
    #print ("NA1 or EUW1 (Note: You can add more regions by just changing up the URL!\n")

    #I first ask the user for three things, their region, summoner name, and API Key.
    #These are the only three things I need from them in order to get create my URL and grab their ID.

    region = "EUW1"
    summonerName = (str)(input('Type your Summoner Name here and DO NOT INCLUDE ANY SPACES: '))
    APIKey = rg_api_key.riot_api_key

    #I send these three pieces off to my requestData function which will create the URL and give me back a JSON that has the ID for that specific summoner.
    #Once again, what requestData returns is a JSON.
    responseJSON  = requestSummonerData(region, summonerName, APIKey)

    #print (responseJSON)
    
    ID = responseJSON['id']
    ID = str(ID)
    print(ID)

    accountID = responseJSON['accountId']
    accountID = str(accountID)
    #print (ID)


    responseJSON2 = requestRankedData(region, ID, APIKey)

    #Create a JSON with a list of all matches
    responseJSON3 = requestMatchList(region, accountID, APIKey)

    #get a number of matchIDs of the matchlist JSON and put the matchIDs into a list
    matchIdList = []
    #we don't want the data of more than 50 matches
    if len(responseJSON3['matches']) < 51:
        for i in range(len(responseJSON3['matches'])):
            matchIdList.append(getMatchId(responseJSON3, i))

    else:
        for i in range(50):
            matchIdList.append(getMatchId(responseJSON3, i))

    print(matchIdList)

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

