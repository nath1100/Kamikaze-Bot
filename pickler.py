try:
    import cPickle as pickle
except ImportError:
    import pickle
import datetime, shelve
from cogs.utilities import paths
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
    "sendai" : [72, 77, 83, 88, 94, 105, 110, 116, 121, 138, 143],
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

''' EXPEDITION
#template
# "id":,"name":"","time":,"exp":{"total":{"hq":,"ship":},"hourly":{"hq":,"ship":}},"yield":{"total":[0,0,0,0],"hourly":[0,0,0,0]},"reward":[None, None],"requirements":{"fs":,"total":None,"ships":"","drums":None},"consumption":[0,0]

expedition_data = {
    "1": {"id":1,"name":"練習航海","time":15,"exp":{"total":{"hq":10,"ship":10},"hourly":{"hq":40,"ship":40}},"yield":{"total":[0,30,0,0],"hourly":[0,120,0,0]},"reward":[None, None],"requirements":{"fs":1,"total":None,"ships":"2XX","drums":None},"consumption":[-3,0]},
    "2": {"id":2,"name":"長距離練習航海","time":30,"exp":{"total":{"hq":20,"ship":15},"hourly":{"hq":40,"ship":30}},"yield":{"total":[0,100,30,0],"hourly":[0,200,60,0]},"reward":["Bucket", None],"requirements":{"fs":2,"total":None,"ships":"4XX","drums":None},"consumption":[-5,0]},
    "3": {"id":3,"name":"警備任務","time":20,"exp":{"total":{"hq":30,"ship":30},"hourly":{"hq":90,"ship":90}},"yield":{"total":[30,30,40,0],"hourly":[90,90,120,0]},"reward":[None, None],"requirements":{"fs":3,"total":None,"ships":"3XX","drums":None},"consumption":[-3,-2]},
    "4": {"id":4,"name":"対潜警戒任務","time":50,"exp":{"total":{"hq":30,"ship":40},"hourly":{"hq":36,"ship":48}},"yield":{"total":[0,60,0,0],"hourly":[0,72,0,0]},"reward":["Bucket", "Small coin box"],"requirements":{"fs":3,"total":None,"ships":"1CL, 2DD","drums":None},"consumption":[-5,0]},
    "5": {"id":5,"name":"海上護衛任務","time":90,"exp":{"total":{"hq":40,"ship":40},"hourly":{"hq":26,"ship":26}},"yield":{"total":[200,200,20,20],"hourly":[133,133,13,13]},"reward":[None, None],"requirements":{"fs":3,"total":None,"ships":"1CL, 2DD, 1XX","drums":None},"consumption":[-5,0]},
    "6": {"id":6,"name":"防空射撃演習","time":40,"exp":{"total":{"hq":30,"ship":50},"hourly":{"hq":45,"ship":75}},"yield":{"total":[0,0,0,80],"hourly":[0,0,0,120]},"reward":["Small coin box", None],"requirements":{"fs":4,"total":None,"ships":"4XX","drums":None},"consumption":[-3,-2]},
    "7": {"id":7,"name":"観艦式予行","time":60,"exp":{"total":{"hq":60,"ship":120},"hourly":{"hq":60,"ship":120}},"yield":{"total":[0,0,50,30],"hourly":[0,0,50,30]},"reward":["Flamethrower", None],"requirements":{"fs":5,"total":None,"ships":"6XX","drums":None},"consumption":[-5,0]},
    "8": {"id":8,"name":"観艦式","time":180,"exp":{"total":{"hq":120,"ship":140},"hourly":{"hq":40,"ship":46}},"yield":{"total":[50,100,50,50],"hourly":[16,33,16,16]},"reward":["2x Flamethrower", "DevMat"],"requirements":{"fs":6,"total":None,"ships":"6XX","drums":None},"consumption":[-5,-2]},
    "9": {"id":9,"name":"タンカー護衛任務","time":240,"exp":{"total":{"hq":60,"ship":60},"hourly":{"hq":15,"ship":15}},"yield":{"total":[350,0,0,0],"hourly":[87,0,0,0]},"reward":["Small coin box", "2x Bucket"],"requirements":{"fs":3,"total":None,"ships":"1CL, 2DD, 1XX","drums":None},"consumption":[-5,0]},
    "10": {"id":10,"name":"強行偵察任務","time":90,"exp":{"total":{"hq":40,"ship":50},"hourly":{"hq":26,"ship":33}},"yield":{"total":[0,50,0,30],"hourly":[0,33,0,20]},"reward":["Bucket", "Flamethrower"],"requirements":{"fs":3,"total":None,"ships":"2CL, 1XX","drums":None},"consumption":[-3,0]},
    "11": {"id":11,"name":"ボーキサイト輸送任務","time":300,"exp":{"total":{"hq":40,"ship":40},"hourly":{"hq":8,"ship":8}},"yield":{"total":[0,0,0,250],"hourly":[0,0,0,50]},"reward":["Small coin box", "Bucket"],"requirements":{"fs":6,"total":None,"ships":"2DD, 2XX","drums":None},"consumption":[-5,0]},
    "12": {"id":12,"name":"資源輸送任務","time":480,"exp":{"total":{"hq":60,"ship":50},"hourly":{"hq":7,"ship":6}},"yield":{"total":[50,250,200,50],"hourly":[6,31,25,6]},"reward":["Medium coin box", "DevMat"],"requirements":{"fs":4,"total":None,"ships":"2DD, 2XX","drums":None},"consumption":[-5,0]},
    "13": {"id":13,"name":"鼠輸送作戦","time":240,"exp":{"total":{"hq":70,"ship":60},"hourly":{"hq":17,"ship":15}},"yield":{"total":[240,300,0,0],"hourly":[60,75,0,0]},"reward":["2x Bucket", "Small coin box"],"requirements":{"fs":5,"total":None,"ships":"1CL, 4DD, 1XX","drums":None},"consumption":[-5,-4]},
    "14": {"id":14,"name":"包囲陸戦隊撤収作戦","time":360,"exp":{"total":{"hq":90,"ship":100},"hourly":{"hq":15,"ship":16}},"yield":{"total":[0,240,200,0],"hourly":[0,40,33,0]},"reward":["Bucket", "DevMat"],"requirements":{"fs":6,"total":None,"ships":"1CL, 3DD, 2XX","drums":None},"consumption":[-5,0]},
    "15": {"id":15,"name":"囮機動部隊支援作戦","time":720,"exp":{"total":{"hq":100,"ship":160},"hourly":{"hq":8,"ship":13}},"yield":{"total":[0,0,300,400],"hourly":[0,0,25,33]},"reward":["Large coin box", "DevMat"],"requirements":{"fs":9,"total":None,"ships":"2CV(L)/AV, 2DD, 2XX","drums":None},"consumption":[-5,-4]},
    "16": {"id":16,"name":"艦隊決戦援護作戦","time":900,"exp":{"total":{"hq":120,"ship":200},"hourly":{"hq":8,"ship":13}},"yield":{"total":[500,500,200,200],"hourly":[33,33,13,13]},"reward":["2x Flamethrower", "2x DevMat"],"requirements":{"fs":10,"total":None,"ships":"1CL, 2DD, 3XX","drums":None},"consumption":[-5,-4]},
    "17": {"id":17,"name":"敵地偵察作戦","time":45,"exp":{"total":{"hq":30,"ship":40},"hourly":{"hq":40,"ship":53}},"yield":{"total":[70,70,50,0],"hourly":[93,93,67,0]},"reward":[None, None],"requirements":{"fs":20,"total":None,"ships":"1CL, 3DD, 2XX","drums":None},"consumption":[-3,-4]},
    "18": {"id":18,"name":"航空機輸送作戦","time":300,"exp":{"total":{"hq":60,"ship":60},"hourly":{"hq":12,"ship":12}},"yield":{"total":[0,0,300,100],"hourly":[0,0,60,20]},"reward":["Bucket", None],"requirements":{"fs":15,"total":None,"ships":"3CV(L)/AV, 2DD, 1XX","drums":None},"consumption":[-5,-2]},
    "19": {"id":19,"name":"北号作戦","time":360,"exp":{"total":{"hq":60,"ship":70},"hourly":{"hq":10,"ship":11}},"yield":{"total":[400,0,50,30],"hourly":[67,0,8,5]},"reward":["Small coin box", "DevMat"],"requirements":{"fs":20,"total":None,"ships":"2BBV, 2DD, 2XX","drums":None},"consumption":[-5,-4]},
    "20": {"id":20,"name":"潜水艦哨戒任務","time":120,"exp":{"total":{"hq":40,"ship":50},"hourly":{"hq":20,"ship":25}},"yield":{"total":[0,0,150,0],"hourly":[0,0,75,0]},"reward":["DevMat", "Small coin box"],"requirements":{"fs":1,"total":None,"ships":"1SS(V), 1CL","drums":None},"consumption":[-5,-4]},
    "21": {"id":21,"name":"北方鼠輸送作戦","time":140,"exp":{"total":{"hq":45,"ship":55},"hourly":{"hq":19,"ship":23}},"yield":{"total":[320,270,0,0],"hourly":[137,116,0,0]},"reward":["Small coin box", None],"requirements":{"fs":15,"total":30,"ships":"1CL, 4DD","drums":"3 total across 3 ships"},"consumption":[-8,-7]},
    "22": {"id":22,"name":"艦隊演習","time":180,"exp":{"total":{"hq":45,"ship":400},"hourly":{"hq":15,"ship":133}},"yield":{"total":[0,10,0,0],"hourly":[0,3,0,0]},"reward":[None, None],"requirements":{"fs":30,"total":45,"ships":"1CA, 1CL, 2DD, 2XX","drums":None},"consumption":[-8,-7]},
    "23": {"id":23,"name":"航空戦艦運用演習","time":240,"exp":{"total":{"hq":70,"ship":420},"hourly":{"hq":17,"ship":105}},"yield":{"total":[0,20,0,100],"hourly":[0,5,0,25]},"reward":[None, None],"requirements":{"fs":50,"total":200,"ships":"2BBV, 2DD, 2XX","drums":None},"consumption":[-8,-8]},
    "24": {"id":24,"name":"北方航路海上護衛","time":500,"exp":{"total":{"hq":65,"ship":80},"hourly":{"hq":7.8,"ship":9.6}},"yield":{"total":[500,0,0,150],"hourly":[60,0,0,18]},"reward":["2x DevMat", "Bucket"],"requirements":{"fs":50,"total":200,"ships":"__1CL__, 4DD, 1XX","drums":"None, but drums increase GS chance"},"consumption":[-9,-6]},
    "25": {},
    "26": {},
    "27": {},
    "28": {},
    "29": {},
    "30": {},
    "31": {},
    "32": {},
    "33": {},
    "34": {},
    "35": {},
    "36": {},
    "37": {},
    "38": {},
    "39": {},
    "40": {}
}

with shelve.open("db\\expedition_db\\exped_db", "c") as shelf:
    for exped in expedition_data:
        shelf[exped] = expedition_data[exped]
'''
