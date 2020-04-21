responseMatchList = {
	"matches": [
		{
            "platformId": "EUW1",
            "gameId": 4504199854,
            "champion": 254,
            "queue": 400,
            "season": 13,
            "timestamp": 1585948764577,
            "role": "NONE",
            "lane": "JUNGLE"
        },
        {
            "platformId": "EUW1",
            "gameId": 4504156757,
            "champion": 254,
            "queue": 400,
            "season": 13,
            "timestamp": 1585946185329,
            "role": "NONE",
            "lane": "JUNGLE"
        },
		]
}
matchList_data = []

for i in range(2):
	y = {
            'gameId': responseMatchList['matches'][i]['gameId'],
            'champion': responseMatchList['matches'][i]['champion'],
            'queue': responseMatchList['matches'][i]['queue'],
            'season': responseMatchList['matches'][i]['season'],
            'timestamp': responseMatchList['matches'][i]['timestamp'],
            'role':responseMatchList['matches'][i]['role'],
            'lane': responseMatchList['matches'][i]['lane']
        }
	matchList_data.append(y)

print(matchList_data[0])
for match in matchList_data:
    print(match['gameId'])