list = [[] for j in range(10)]
biglist = [{'hello': 'hello'}]
list[5].append({
    'hi': 'hi',
    })
list2 = {'hi': 'world'}
biglist.update(list2)

print(list2)
print(biglist)