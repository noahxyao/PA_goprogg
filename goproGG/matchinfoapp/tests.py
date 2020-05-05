matchDetailInfo_Dict = {}
keys = range(10)
for key in keys:
    matchDetailInfo_Dict[str(key)] = key

print(matchDetailInfo_Dict)

keyList = [i+1 for i in range(10)]
print(keyList)

newDict = dict(zip(keyList, list(matchDetailInfo_Dict.values())))

print(newDict)

for i in newDict:
    print(i)