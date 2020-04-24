from pantheon import pantheon
import asyncio
import rg_api_key

server = "euw1"
api_key = rg_api_key.riot_api_key

def requestsLog(url, status, headers):
    print(url)
    print(status)
    print(headers)

panth = pantheon.Pantheon(server, api_key, errorHandling=True, requestsLoggingFunction=requestsLog, debug=True)

async def getSummonerId(name):
    try:
        data = await panth.getSummonerByName(name)
        return (data['id'],data['accountId'])
    except Exception as e:
        print(e)


async def getRecentMatchlist(accountId):
    try:
        data = await panth.getMatchlist(accountId, params={"endIndex":10})
        return data
    except Exception as e:
        print(e)

async def getRecentMatches(accountId):
    try:
        matchlist = await getRecentMatchlist(accountId)
        tasks = [panth.getMatch(match['gameId']) for match in matchlist['matches']]
        return await asyncio.gather(*tasks)
    except Exception as e:
        print(e)

async def getRecentTimeline(accountId):
    try:
        matchlist = await getRecentMatchlist(accountId)
        tasks = [panth.getTimeline(match['gameId']) for match in matchlist['matches']]
        return await asyncio.gather(*tasks)
    except Exception as e:
        print(e)


name = "exkira"

loop = asyncio.get_event_loop()  

(summonerId, accountId) = loop.run_until_complete(getSummonerId(name))
print(summonerId)
print(accountId)
loop.run_until_complete(getRecentTimeline(accountId))

# print(tasks[0]['frames'][0]['participantFrames']['1'][1]['currentGold'])