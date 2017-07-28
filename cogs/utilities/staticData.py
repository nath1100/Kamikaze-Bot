"""
This utility module is used to store static data that does not ever change.
Cogs can import this to utilise data.
Should not be used for data that can change and requires persistence, such as the doomsday command.
"""

def airPower(world : int, level : int):
    """Receive world info and output minimum AS info."""
    #data table: data[world][level][node][0:AS, 1:AS+]
    data = {
        1: {
            1:{'A':[0,0], 'B':[0,0], 'C':[0,0]},
            2:{'A':[0,0], 'B':[0,0], 'D':[0,0]},
            3:{'A':[0,0], 'E':[0,0], 'F':[0,0], 'G':[0,0]},
            4:{'A':[0,0], 'B':[0,0], 'E':[24,48], 'F':[30,60], 'I':[24,48], 'J':[0,0]},
            5:{'A':[0,0], 'B':[0,0], 'C':[0,0], 'D':[0,0], 'F':[0,0], 'G':[0,0], 'I':[0,0]},
            6:{'B':[36,72], 'C':[0,0], 'D':[198,396], 'E':[0,0], 'F':[83,165], 'I':[0,0], 'J':[177,354], 'K':[0,0], 'L':[288,576]}
        },
        2: {
            1:{'A':[0,0], 'C':[36,72], 'E':[42,84], 'F':[36,72]},
            2:{'A':[0,0], 'D':[0,0], 'F':[81,162], 'G':[0,0]},
            3:{'B':[0,0], 'C':[0,0], 'F':[0,0], 'G':[56,111], 'H':[39,78], 'K':[39,78]},
            4:{'A':[0,0], 'C':[0,0], 'D':[123,246], 'F':[0,0], 'G':[102,204], 'H':[123,246], 'I':[0,0], 'J':[0,0], 'L':[0,0], 'N':[123,246], 'O':[0,0], 'P':[123,246]},
            5:{'A':[0,0], 'B':[35,69], 'D':[0,0], 'E':[0,0], 'I':[153,306], 'J':[0,0], 'L':[0,0]}
        },
        3: {
            1:{'A':[0,0], 'C':[108,216], 'D':[0,0], 'E':[42,84], 'F':[108,216]},
            2:{'A':[0,0], 'C':[117,234], 'E':[0,0], 'F':[0,0], 'H':[0,0]},
            3:{'A':[0,0], 'C':[108,216], 'D':[119,237], 'E':[108,216], 'G':[83,165], 'I':[119,237]},
            4:{'A':[0,0], 'B':[72,144], 'D':[123,246], 'E':[84,168], 'F':[72,144], 'H':[0,0], 'I':[123,246], 'J':[0,0], 'L':[72,144], 'N':[1234,246]},
            5:{'A':[0,0], 'B':[0,0], 'C':[321,642], 'E':[35,69], 'F':[381,762], 'G':[35,69], 'K':[0,0]}
        },
        4: {
            1:{'A':[0,0], 'B':[0,0], 'C':[0,0], 'D':[72,144], 'E':[0,0], 'G':[0,0], 'H':[0,0], 'I':[0,0]},
            2:{'A':[0,0], 'C':[0,0], 'D':[42,84], 'F':[0,0], 'H':[113,216], 'I':[36,72]},
            3:{'A':[72,144], 'D':[0,0], 'F':[0,0], 'G':[114,228], 'I':[42,84], 'J':[72,144], 'K':[0,0], 'M':[42,84]},
            4:{'A':[0,0], 'C':[114,228], 'F':[72,144], 'G':[156,312], 'H':[153,306], 'I':[72,144], 'J':[114,228]},
            5:{'C':[0,0], 'D':[0,0], 'E':[0,0], 'A':[0,0], 'F':[0,0], 'H':[252,504], 'I':[0,0], 'J':[35,69], 'M':[207,414]}
        },
        5: {
            1:{'A':[36,72], 'D':[0,0], 'E':[156,312], 'F':[36,72], 'H':[108,216], 'I':[42,84]},
            2:{'A':[0,0], 'B':[36,72], 'C':[42,84], 'D':[146,291], 'F':[36,72], 'G':[0,0], 'I':[0,0], 'J':[42,84]},
            3:{'B':[0,0], 'C':[0,0], 'D':[0,0], 'E':[114,228], 'F':[0,0], 'J':[42,84], 'K':[113,225]},
            4:{'A':[36,72], 'C':[42,84], 'F':[0,0], 'G':[42,84], 'H':[174,348], 'I':[36,72], 'K':[153,306], 'N':[0,0], 'O':[114,228]},
            5:{'A':[210,420], 'B':[210,420], 'C':[35,69], 'D':[257,513], 'E':[161,321], 'F':[35,69], 'G':[161,321], 'H':[161,321], 'K':[302,603], 'M':[35,69], 'N':[377,753]}
        },
        6: {
            1:{'B':[35,69], 'C':[0,0], 'D':[0,0], 'F':[0,0], 'H':[270,540], 'J':[0,0], 'K':[126,252]},
            2:{'A':[72,144], 'B':[69,138], 'E':[252,504], 'G':[35,69], 'H':[35,69], 'I':[153,306], 'K':[126,252]},
            3:{'B':[0,0], 'C':[0,0], 'D':[0,0], 'E':[0,0], 'F':[0,0], 'J':[0,0], },
            4:{'A':[0,0], 'B':[0,0], 'C':[36,72], 'D':[123,246], 'E':[0,0], 'F':[177,334], 'G':[123,246], 'H':[36,72], 'I':[158,315], 'J':[198,396], 'K':[189,378], 'L':[69,138], 'M':[0,0], 'N':[168,336]},
            5:{'A':[0,0], 'B':[0,0], 'C':[198,396], 'D':[69,138], 'E':[0,0], 'F':[0,0], 'G':[468,936], 'H':[309,618], 'I':[69,138], 'J':[35,69], 'M':[468,936]}
        }
    }

    return data[world][level]


def sigmaValues(battleship):
    """Contains sigma values of BBs for WoWs. Returns string sigma"""
    data = {
        'south carolina':1.8,
        'wyoming':1.5,
        'arkansas beta':1.5,
        'new york':1.8,
        'texas':1.8,
        'new mexico':1.5,
        'arizona':1.8,
        'colorado':2.0,
        'colorado a':1.8,
        'north carolina':2.0,
        'iowa':1.9,
        'montana':1.9,
        'mikasa':1.8,
        'kawachi':1.8,
        'myogi':1.8,
        'ishizuchi':2.0,
        'kongo':1.8,
        'fuso':1.5,
        'nagato':2.0,
        'amagi':1.8,
        'izumo':1.8,
        'yamato':2.1,
        'nassasu':1.8,
        'konig albert':1.8,
        'kaiser':1.8,
        'konig':2.0,
        'bayern':1.8,
        'gneisenau':1.8,
        'scharnhorst':2.0,
        'bismarck':1.8,
        'tirpitz':1.8,
        'friedrich der grobe':1.8,
        'friedrich':1.8,
        'grosser kurfurst':1.8,
        'kurfurst':1.8,
        'warspite':2.0,
        'imperator nikolai i':2.0,
        'nikolai':2.0,
        'dunkerque':1.7,
        'missouri':1.9,
        'high_tier_cruisers':2.05
    }

    high_cruisers = ['ibuki', 'zao', 'baltimore', 'des moine', 'roon', 'hindenburg', 'neptune', 'minotaur', 'dmitry donskoy', 'moskva']

    try:
        return data[battleship]
    except KeyError:
        if battleship in high_cruisers:
            return data['high_tier_cruisers']

def lbasRangeData(shortest_range : int):
    """Contains range data for LBAS; returns range dictionary"""
    data ={
        "Type 2 Large Flying Boat": ["", "", 3, 3, 3, 3, 3, 3, 3, 3],
        "PBY-5A Catalina": ["","", 3, 3, 2, 2, 2, 2, 1, 1],
        "Prototype Keiun (Recon)": ["", "", 2, 2, 2, 2, 1, 1, 0, 0],
        "Saiun": ["", "", 2, 2, 2, 2, 1, 1, 0, 0],
        "Type 0 Recon Seaplane": ["", "", 2, 2, 2, 1, 1, 0, 0, 0],
        "Type 2 Recon Aircraft": ["", "", 2, 1, 1, 0, 0, 0, 0, 0]
    }

    result = {}
    for x in data:
        result[x] = data[x][int(shortest_range)]
    return result
