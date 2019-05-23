from impl.persisted_dict import PersistedDict

myDictionary = PersistedDict('persist')
myDictionary['a'] = {1: [1, 2, 3, 4]}
print(myDictionary.keys())

print(myDictionary['a'])
myDictionary.clear()
