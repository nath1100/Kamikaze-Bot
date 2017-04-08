try:
    import cPickle as pickle
except ImportError:
    import pickle
import datetime
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

'''
doomsday_target = {"260977178131431425":[datetime.datetime(year=2050, month=12, day=31, hour=23, minute=59, second=59), 'remain']}

with open('doomsday_target.pickle', 'wb') as f:
    pickle.dump(doomsday_target, f)
'''

''' OASW
oasw_database = {
    "asashio kai ni d" : [85, 85, 85, 85, 85, 85, 85, 85, 85, 97, 102],
    "libeccio kai" : [60, 65, 70, 75, 80, 90, 95, 99, 104, 119, 124],
    "satsuki kai ni" : [75, 75, 75, 78, 82, 90, 94, 98, 101, 113, 117],
    "asashimo kai" : [66, 70, 75, 79, 84, 93, 97, 102, 106, 120, 124],
    "ushio kai ni" : [74, 79, 83, 88, 93, 102, 106, 111, 116, 129, 134],
    "verniy" : [77, 81, 86, 90, 95, 104, 108, 113, 117, 131, 135],
    "akizuki kai" : [81, 85, 90, 95, 99, 109, 114, 118, 123, 137, 142],
    "teruzuki kai" : [81, 85, 90, 95, 99, 109, 114, 118, 123, 137, 142],
    "hatsuzuki kai" : [81, 85, 90, 95, 99, 109, 114, 118, 123, 137, 142],
    "shigure kai ni" : [83, 87, 92, 97, 102, 112, 116, 121, 126, 141, 145],
    "yuudachi kai ni" : [87, 92, 97, 102, 107, 116, 121, 126, 131, 145, 150],
    "murakumo kai ni" : [87, 92, 97, 102, 107, 116, 121, 126, 131, 145, 150],
    "hatsushimo kai ni" : [87, 92, 97, 102, 107, 116, 121, 126, 131, 145, 150],
    "mutsuki kai ni" : [87, 92, 97, 102, 107, 116, 121, 126, 131, 145, 150],
    "hatsuharu kai ni" : [87, 92, 97, 102, 107, 117, 122, 127, 132, 148, 153],
    "kisaragi kai ni" : [88, 92, 97, 102, 107, 116, 121, 125, 130, 144, 149],
    "fubuki kai ni" : [90, 95, 99, 104, 109, 118, 123, 128, 132, 147, 151],
    "kasumi kai ni" : [90, 95, 99, 104, 109, 119, 124, 129, 134, 149, 154],
    "akatsuki kai ni" : [94, 99, 104, 110, 115, 126, 131, 136, 141, 'N/A', 'N/A'],
    "ooshio kai ni" : [99, 105, 110, 115, 120, 131, 136, 141, 146, 'N/A', 'N/A'],
    "ayanami kai ni" : [102, 107, 113, 118, 123, 133, 139, 144, 149, 'N/A', 'N/A'],
    "kawakaze kai ni" : [102, 107, 113, 118, 123, 133, 139, 144, 149, 'N/A', 'N/A'],
    "arashio kai ni" : [144, 120, 126, 132, 138, 150, 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'],
    "shimakaze kai" : [115, 121, 127, 134, 140, 152, 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'],
    "yukikaze kai" : [115, 121, 127, 134, 140, 152, 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'],
    "kinu kai ni" : [75, 75, 75, 75, 75, 75, 80, 86, 91, 108, 113],
    "naka kai ni" : [48, 80, 88, 61, 66, 77, 83, 88, 94, 110, 116],
    "sakawa kai" : [63, 66, 70, 74, 77, 85, 88, 92, 96, 107, 110],
    "abukuma kai ni" : [75, 75, 75, 75, 75, 82, 88, 94, 99, 117, 123],
    "kiso kai ni" : [65, 68, 72, 76, 80, 88, 92, 96, 99, 111, 115],
    "agano kai" : [68, 71, 75, 78, 82, 89, 92, 96, 99, 110, 114],
    "noshiro kai" : [68, 71, 75, 78, 82, 89, 92, 96, 99, 110, 114],
    "yahagi kai" : [68, 71, 75, 78, 82, 89, 92, 96, 99, 110, 114],
    "jintsuu kai ni" : [60, 65, 70, 75, 80, 90, 95, 99, 104, 119, 124],
    "yura kai" : [52, 58, 64, 71, 77, 90, 96, 103, 109, 128, 135],
    "kitakami kai ni" : [71, 75, 79, 82, 86, 94, 98, 101, 105, 117, 120],
    "ooi kai ni" : [71, 75, 79, 82, 86, 94, 98, 101, 105, 117, 120],
    "kuma kai" : [72, 76, 80, 83, 87, 94, 98, 101, 105, 116, 119],
    "tama kai" : [72, 76, 80, 83, 87, 94, 98, 101, 105, 116, 119],
    "natori kai" : [72, 76, 80, 83, 87, 94, 98, 101, 105, 116, 119],
    "sendai kai ni" : [72, 77, 83, 88, 94, 105, 11, 116, 121, 138, 143],
    "tenryuu kai" : [88, 93, 97, 102, 106, 115, 119, 124, 129, 141, 146],
    "tatsuta kai" : [88, 93, 97, 102, 106, 115, 119, 124, 129, 141, 146],
    "yuubari kai" : [62, 66, 71, 75, 80, 84, 88, 93, 97, 102, 106, 115, 119, 124, 129, 141, 146],
    "kashima kai" : [62, 66, 71, 75, 80, 84, 88, 93, 97, 102, 106, 115, 119, 124, 129, 141, 146],
    "katori kai" : [75, 80, 85, 90, 95, 99, 104, 109, 114, 119, 124, 134, 139, 144, 149, 'N/A', 'N/A'],
    "ooyodo kai" : [132, 138, 143, 148, 153, 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A']
}

with open('oasw_database.pickle', 'wb') as f:
    pickle.dump(oasw_database, f)
'''
