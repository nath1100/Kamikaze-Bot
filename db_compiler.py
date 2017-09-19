import shelve, json

def loadRawData():
    with open('ship_db_raw', 'rb') as f:
        rawData = f.read().decode('utf-8').replace('\r','').split('\n')
        shipData = [json.loads(x) for x in rawData]
    with open('ship_namesuffix_db_raw', 'rb') as f:
        rawData = f.read().decode('utf-8').replace('\r','').split('\n')
        suffixData = [json.loads(x) for x in rawData]
    return (shipData, suffixData)

def fixSuffix(suffix : str):
    """Enter a suffix and translate it to wikia standards"""
    specialCases = {
        "два": "Dva",
        "kou": "Carrier",
        "Kaibu": "Bo",
        "Kou": "A",
        "Otsu": "B",
        "Chou": "D"
    }
    #if any(case in suffix for case in specialCases):
    for case in specialCases:
        if  case in suffix:
            return suffix.replace(case, specialCases[case])
    return suffix

def fixShipName(dictionary):
    """Pass dictionary, return proper ship name"""
    # this list identifies same-name ships (like the fog ships) in terms of romaji
    specialCases_romaji = [
        'haruna',
        'takao'
    ]
    # this list identifies english translations of JA_JP names when JA_ROMAJI cannot be used
    specialCases = {
        "タカオ": "Takao (fog)",
        "ハルナ": "Haruna (fog)",
        "Гангут": "Gangut",
        "水無月": "Minazuki",
        "Октябрьская революция": "Gangut kai",
        "Верный": "Verniy",
        "伊504": "i-504"
    }
    # this list identifies name-fixes to otherwise functioning JA_ROMAJI names
    hardCodedCases = {
        "shimusyu": "shimushu"
    }
    name = dictionary['name']
    # first check if the name has no JA_ROMAJI
    if name['ja_romaji'] == "":
        # check if the name in the special cases list
        if name['ja_jp'] in specialCases:
            # return the fixed name
            return specialCases[name['ja_jp']]
        else:
            # otherwise, return its JA_JP name (for cases like Z1, Z3, etc)
            return name['ja_jp']
    elif name['ja_romaji'] in specialCases_romaji and name['ja_jp'] in specialCases: # account for the fog ships
        return specialCases[name['ja_jp']]
    # otherwise, if it does have JA_ROMAJI....
    else:
        # check if the JA_ROMAJI should be fixed
        if name["ja_romaji"] in hardCodedCases:
            return hardCodedCases[name["ja_romaji"]]
        # otherwise, simply return the JA_ROMAJI
        else:
            return name['ja_romaji']

def addSuffix(dictionary):
    """Pass dictionary, return a suffix if any"""
    suffixID = dictionary['name']['suffix']
    if suffixID is not None:
        return " " + suffixDict[suffixID]
    else:
        return ""

def organiseStats(dictionary):
    """Pass dictionary, return appropriate stats dict"""
    d = {**dictionary['stat'], **dictionary['consum']}
    d['base_lvl'] = dictionary['base_lvl']
    d['slot'] = str(dictionary['slot']).strip('[]')
    d['id'] = dictionary['id']
    return d

#load data as list of dicts
shipData, suffixData = loadRawData()
#create suffix dictionary
suffixDict = {}
for x in suffixData:
   suffixDict[x['id']] = fixSuffix(x['ja_romaji'])

''' #testing output
testDictionary = {}
for ship in shipData:
    testDictionary[fixShipName(ship).lower() + addSuffix(ship).lower()] = organiseStats(ship)
for x in testDictionary: print("{}: {}".format(x, testDictionary[x]))
'''

#shelf construction
with shelve.open("db\\ship_db", "c") as shelf:
    for ship in shipData:
        shelf[fixShipName(ship).lower() + addSuffix(ship).lower()] = organiseStats(ship)
    # Add the base 0 comparator
    shelf['0_stat'] = {"fire_max":0,"torpedo_max":0,"aa_max":0,"asw_max":0,"hp":0,"armor_max":0,"evasion_max":0,"luck":0,"fuel":0,"ammo":0,"base_lvl":0, "slot":""}

''' #shelf retrieval test
target = input("Kanmusu: ")
with shelve.open('db\\ship_db', 'r') as shelf:
    data = shelf[target]
print(data)
input()
'''

# Finished output
input("Compile finished. ENTER to quit.")
