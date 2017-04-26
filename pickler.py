try:
    import cPickle as pickle
except ImportError:
    import pickle
import datetime

''' COUNTDOWN
countdown_all = {}
with open('countdown_all.pickle', 'wb') as f:
    pickle.dump(countdown_all, f)
'''

''' COIN STASH
coin_stash = {'178112312845139969':0}
with open('coin_stash.pickle', 'wb') as f:
    pickle.dump(coin_stash, f)
'''

''' NOTEPAD
notepad = {}
with open('notepad.pickle', 'wb') as f:
    pickle.dump(notepad, f)
'''

''' KAMIKAZE KEYWORD
kamikaze_chime = {"260977178131431425":True}
with open('kamikaze_chime.pickle', 'wb') as f:
    pickle.dump(kamikaze_chime, f)
'''

''' NSFW ENABLED CHANNELS
nsfwChannels = []
with open('nsfwChannels.pickle','wb') as f:
    pickle.dump(nsfwChannels, f)
'''

''' SOKU IP LIST
soku_ip = {}
with open('soku_ip.pickle','wb') as f:
    pickle.dump(soku_ip, f)
'''
    
''' STATUS
kamikaze_status = ["Waiting for the event"]
with open('kamikaze_status.pickle', 'wb') as f:
    pickle.dump(kamikaze_status, f)
'''

''' OASW
oasw_database = {
    11 : ['T4/T4/T4', 'T4/T4/T3', 'T4/T4/DC', 'T4/T3/DC', 'T3/T3/DC', 'T4/T4', 'T4/T3', 'T4/DC', 'T3/DC', 'T4', 'T3'],
    17 : ['T4/T4/T4/T4', 'T4/T4/T4/T3', 'T4/T4/T4/DC', 'T4/T4/T3/DC', 'T4/T3/T3/DC', 'T3/T3/T3/DC', 'T4/T4/T4', 'T4/T4/T3', 'T4/T4/DC', 'T4/T3/DC', 'T3/T3/DC', 'T4/T4', 'T4/T3', 'T4/DC', 'T3/DC', 'T4', 'T3'],
    "asashio" : [85, 85, 85, 85, 85, 85, 85, 85, 85, 97, 102],
    "libeccio" : [60, 65, 70, 75, 80, 90, 95, 99, 104, 119, 124],
    "satsuki" : [75, 75, 75, 78, 82, 90, 94, 98, 101, 113, 117],
    "asashimo" : [66, 70, 75, 79, 84, 93, 97, 102, 106, 120, 124],
    "ushio" : [74, 79, 83, 88, 93, 102, 106, 111, 116, 129, 134],
    "verniy" : [77, 81, 86, 90, 95, 104, 108, 113, 117, 131, 135],
    "bep" : [77, 81, 86, 90, 95, 104, 108, 113, 117, 131, 135],
    "akizuki" : [81, 85, 90, 95, 99, 109, 114, 118, 123, 137, 142],
    "teruzuki" : [81, 85, 90, 95, 99, 109, 114, 118, 123, 137, 142],
    "hatsuzuki" : [81, 85, 90, 95, 99, 109, 114, 118, 123, 137, 142],
    "shigure" : [83, 87, 92, 97, 102, 112, 116, 121, 126, 141, 145],
    "yuudachi" : [87, 92, 97, 102, 107, 116, 121, 126, 131, 145, 150],
    "murakumo" : [87, 92, 97, 102, 107, 116, 121, 126, 131, 145, 150],
    "hatsushimo" : [87, 92, 97, 102, 107, 116, 121, 126, 131, 145, 150],
    "mutsuki" : [87, 92, 97, 102, 107, 116, 121, 126, 131, 145, 150],
    "hatsuharu" : [87, 92, 97, 102, 107, 117, 122, 127, 132, 148, 153],
    "kisaragi" : [88, 92, 97, 102, 107, 116, 121, 125, 130, 144, 149],
    "fubuki" : [90, 95, 99, 104, 109, 118, 123, 128, 132, 147, 151],
    "kasumi" : [90, 95, 99, 104, 109, 119, 124, 129, 134, 149, 154],
    "akatsuki" : [94, 99, 104, 110, 115, 126, 131, 136, 141, 'N/A', 'N/A'],
    "ooshio" : [99, 105, 110, 115, 120, 131, 136, 141, 146, 'N/A', 'N/A'],
    "ayanami" : [102, 107, 113, 118, 123, 133, 139, 144, 149, 'N/A', 'N/A'],
    "kawakaze" : [102, 107, 113, 118, 123, 133, 139, 144, 149, 'N/A', 'N/A'],
    "arashio" : [114, 120, 126, 132, 138, 150, 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'],
    "shimakaze" : [115, 121, 127, 134, 140, 152, 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'],
    "yukikaze" : [115, 121, 127, 134, 140, 152, 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'],
    "kinu" : [75, 75, 75, 75, 75, 75, 80, 86, 91, 108, 113],
    "naka" : [48, 80, 88, 61, 66, 77, 83, 88, 94, 110, 116],
    "sakawa" : [63, 66, 70, 74, 77, 85, 88, 92, 96, 107, 110],
    "abukuma" : [75, 75, 75, 75, 75, 82, 88, 94, 99, 117, 123],
    "kiso" : [65, 68, 72, 76, 80, 88, 92, 96, 99, 111, 115],
    "agano" : [68, 71, 75, 78, 82, 89, 92, 96, 99, 110, 114],
    "noshiro" : [68, 71, 75, 78, 82, 89, 92, 96, 99, 110, 114],
    "yahagi" : [68, 71, 75, 78, 82, 89, 92, 96, 99, 110, 114],
    "jintsuu" : [60, 65, 70, 75, 80, 90, 95, 99, 104, 119, 124],
    "yura" : [52, 58, 64, 71, 77, 90, 96, 103, 109, 128, 135],
    "kitakami" : [71, 75, 79, 82, 86, 94, 98, 101, 105, 117, 120],
    "ooi" : [71, 75, 79, 82, 86, 94, 98, 101, 105, 117, 120],
    "kuma" : [72, 76, 80, 83, 87, 94, 98, 101, 105, 116, 119],
    "tama" : [72, 76, 80, 83, 87, 94, 98, 101, 105, 116, 119],
    "natori" : [72, 76, 80, 83, 87, 94, 98, 101, 105, 116, 119],
    "sendai" : [72, 77, 83, 88, 94, 105, 11, 116, 121, 138, 143],
    "tenryuu" : [88, 93, 97, 102, 106, 115, 119, 124, 129, 141, 146],
    "tatsuta" : [88, 93, 97, 102, 106, 115, 119, 124, 129, 141, 146],
    "yuubari" : [62, 66, 71, 75, 80, 84, 88, 93, 97, 102, 106, 115, 119, 124, 129, 141, 146],
    "kashima" : [62, 66, 71, 75, 80, 84, 88, 93, 97, 102, 106, 115, 119, 124, 129, 141, 146],
    "katori" : [75, 80, 85, 90, 95, 99, 104, 109, 114, 119, 124, 134, 139, 144, 149, 'N/A', 'N/A'],
    "ooyodo" : [132, 138, 143, 148, 153, 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A']
}

with open('oasw_database.pickle', 'wb') as f:
    pickle.dump(oasw_database, f)
'''