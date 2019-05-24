from persistent_dict.persisted_dict import PersistenceDict

myDictionary = PersistenceDict('persist')
myDictionary['a'] = {1: [1, 2, 3, 4]}
print(myDictionary.keys())

print(myDictionary['a'])
myDictionary.clear()
