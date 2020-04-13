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
    #print (ID)
    responseJSON2 = requestRankedData(region, ID, APIKey)


    if len(responseJSON2) > 1:

        if responseJSON2[0]['queueType'] == "RANKED_SOLO_5x5":
            print ("Solo Q Information: ")
            print (responseJSON2[0]['tier'])
            print (responseJSON2[0]['rank'])
            print (str(responseJSON2[0]['leaguePoints']) + " LP")

            print ("Flex Q Information: ")
            print (responseJSON2[1]['tier'])
            print (responseJSON2[1]['rank'])
            print (str(responseJSON2[1]['leaguePoints']) + " LP")


        else:
            print ("Flex Q Information: ")
            print (responseJSON2[0]['tier'])
            print (responseJSON2[0]['rank'])
            print (str(responseJSON2[0]['leaguePoints']) + " LP")

            print ("Solo Q Information: ")
            print (responseJSON2[1]['tier'])
            print (responseJSON2[1]['rank'])
            print (str(responseJSON2[1]['leaguePoints']) + " LP")

    elif  len(responseJSON2) == 1:

        if responseJSON2[0]['queueType'] == "RANKED_SOLO_5x5":
            print ("Solo Q Information: ")
            print (responseJSON2[0]['tier'])
            print (responseJSON2[0]['rank'])
            print (str(responseJSON2[0]['leaguePoints']) + " LP")
            print ("This Summoner is unranked in Flex Q")

        else:
            print ("Flex Q Information: ")
            print (responseJSON2[0]['tier'])
            print (responseJSON2[0]['rank'])
            print (str(responseJSON2[0]['leaguePoints']) + " LP")
            print ("This Summoner is unranked in Solo Q")

    else:

        print("This Summoner is unranked in both Solo and Flex Q")



#This starts my program!
if __name__ == "__main__":
    main()

