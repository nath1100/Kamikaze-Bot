try:
    import cPickle as pickle
except ImportError:
    import pickle

import datetime, shelve

from cogs.utilities import paths # For legacy
from cogs.utilities.paths import Path

# # COUNTDOWN
# countdown_all = {}
# with open('countdown_all.pickle', 'wb') as f:
#     pickle.dump(countdown_all, f)


# # COIN STASH
# coin_stash = {'178112312845139969':0}
# with open('coin_stash.pickle', 'wb') as f:
#     pickle.dump(coin_stash, f)


# # NOTEPAD
# notepad = {}
# with open('notepad.pickle', 'wb') as f:
#     pickle.dump(notepad, f)


# # KAMIKAZE KEYWORD
# kamikaze_chime = {"260977178131431425":True}
# with open('kamikaze_chime.pickle', 'wb') as f:
#     pickle.dump(kamikaze_chime, f)


# # NSFW ENABLED CHANNELS
# nsfwChannels = []
# with open('nsfwChannels.pickle','wb') as f:
#     pickle.dump(nsfwChannels, f)


# # SOKU IP LIST
# soku_ip = {}
# with open('soku_ip.pickle','wb') as f:
#     pickle.dump(soku_ip, f)

    
# # STATUS
# kamikaze_status = ["Waiting for the event"]
# with open('kamikaze_status.pickle', 'wb') as f:
#     pickle.dump(kamikaze_status, f)

# # OASW
# oasw_database = {
#     11 : ['T4/T4/T4', 'T4/T4/T3', 'T4/T4/DC', 'T4/T3/DC', 'T3/T3/DC', 'T4/T4', 'T4/T3', 'T4/DC', 'T3/DC', 'T4', 'T3'],
#     17 : ['T4/T4/T4/T4', 'T4/T4/T4/T3', 'T4/T4/T4/DC', 'T4/T4/T3/DC', 'T4/T3/T3/DC', 'T3/T3/T3/DC', 'T4/T4/T4', 'T4/T4/T3', 'T4/T4/DC', 'T4/T3/DC', 'T3/T3/DC', 'T4/T4', 'T4/T3', 'T4/DC', 'T3/DC', 'T4', 'T3'],
#     "asashio" : [85, 85, 85, 85, 85, 85, 85, 85, 85, 97, 102],
#     "libeccio" : [60, 65, 70, 75, 80, 90, 95, 99, 104, 119, 124],
#     "satsuki" : [75, 75, 75, 78, 82, 90, 94, 98, 101, 113, 117],
#     "asashimo" : [66, 70, 75, 79, 84, 93, 97, 102, 106, 120, 124],
#     "ushio" : [74, 79, 83, 88, 93, 102, 106, 111, 116, 129, 134],
#     "verniy" : [77, 81, 86, 90, 95, 104, 108, 113, 117, 131, 135],
#     "bep" : [77, 81, 86, 90, 95, 104, 108, 113, 117, 131, 135],
#     "akizuki" : [81, 85, 90, 95, 99, 109, 114, 118, 123, 137, 142],
#     "teruzuki" : [81, 85, 90, 95, 99, 109, 114, 118, 123, 137, 142],
#     "hatsuzuki" : [81, 85, 90, 95, 99, 109, 114, 118, 123, 137, 142],
#     "shigure" : [83, 87, 92, 97, 102, 112, 116, 121, 126, 141, 145],
#     "yuudachi" : [87, 92, 97, 102, 107, 116, 121, 126, 131, 145, 150],
#     "murakumo" : [87, 92, 97, 102, 107, 116, 121, 126, 131, 145, 150],
#     "hatsushimo" : [87, 92, 97, 102, 107, 116, 121, 126, 131, 145, 150],
#     "mutsuki" : [87, 92, 97, 102, 107, 116, 121, 126, 131, 145, 150],
#     "hatsuharu" : [87, 92, 97, 102, 107, 117, 122, 127, 132, 148, 153],
#     "kisaragi" : [88, 92, 97, 102, 107, 116, 121, 125, 130, 144, 149],
#     "fubuki" : [90, 95, 99, 104, 109, 118, 123, 128, 132, 147, 151],
#     "kasumi" : [90, 95, 99, 104, 109, 119, 124, 129, 134, 149, 154],
#     "akatsuki" : [94, 99, 104, 110, 115, 126, 131, 136, 141, 'N/A', 'N/A'],
#     "ooshio" : [99, 105, 110, 115, 120, 131, 136, 141, 146, 'N/A', 'N/A'],
#     "ayanami" : [102, 107, 113, 118, 123, 133, 139, 144, 149, 'N/A', 'N/A'],
#     "kawakaze" : [102, 107, 113, 118, 123, 133, 139, 144, 149, 'N/A', 'N/A'],
#     "arashio" : [114, 120, 126, 132, 138, 150, 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'],
#     "shimakaze" : [115, 121, 127, 134, 140, 152, 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'],
#     "yukikaze" : [115, 121, 127, 134, 140, 152, 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'],
#     "kinu" : [75, 75, 75, 75, 75, 75, 80, 86, 91, 108, 113],
#     "naka" : [48, 80, 88, 61, 66, 77, 83, 88, 94, 110, 116],
#     "sakawa" : [63, 66, 70, 74, 77, 85, 88, 92, 96, 107, 110],
#     "abukuma" : [75, 75, 75, 75, 75, 82, 88, 94, 99, 117, 123],
#     "kiso" : [65, 68, 72, 76, 80, 88, 92, 96, 99, 111, 115],
#     "agano" : [68, 71, 75, 78, 82, 89, 92, 96, 99, 110, 114],
#     "noshiro" : [68, 71, 75, 78, 82, 89, 92, 96, 99, 110, 114],
#     "yahagi" : [68, 71, 75, 78, 82, 89, 92, 96, 99, 110, 114],
#     "jintsuu" : [60, 65, 70, 75, 80, 90, 95, 99, 104, 119, 124],
#     "yura" : [52, 58, 64, 71, 77, 90, 96, 103, 109, 128, 135],
#     "kitakami" : [71, 75, 79, 82, 86, 94, 98, 101, 105, 117, 120],
#     "ooi" : [71, 75, 79, 82, 86, 94, 98, 101, 105, 117, 120],
#     "kuma" : [72, 76, 80, 83, 87, 94, 98, 101, 105, 116, 119],
#     "tama" : [72, 76, 80, 83, 87, 94, 98, 101, 105, 116, 119],
#     "natori" : [72, 76, 80, 83, 87, 94, 98, 101, 105, 116, 119],
#     "sendai" : [72, 77, 83, 88, 94, 105, 110, 116, 121, 138, 143],
#     "tenryuu" : [88, 93, 97, 102, 106, 115, 119, 124, 129, 141, 146],
#     "tatsuta" : [88, 93, 97, 102, 106, 115, 119, 124, 129, 141, 146],
#     "yuubari" : [62, 66, 71, 75, 80, 84, 88, 93, 97, 102, 106, 115, 119, 124, 129, 141, 146],
#     "kashima" : [62, 66, 71, 75, 80, 84, 88, 93, 97, 102, 106, 115, 119, 124, 129, 141, 146],
#     "katori" : [75, 80, 85, 90, 95, 99, 104, 109, 114, 119, 124, 134, 139, 144, 149, 'N/A', 'N/A'],
#     "ooyodo" : [132, 138, 143, 148, 153, 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A']
# }

# with open('oasw_database.pickle', 'wb') as f:
#     pickle.dump(oasw_database, f)

# #template
# # "id":,"name":"","time":,"exp":{"total":{"hq":,"ship":},"hourly":{"hq":,"ship":}},"yield":{"total":[0,0,0,0],"hourly":[0,0,0,0]},"reward":[None, None],"requirements":{"fs":,"total":None,"ships":"","drums":None},"consumption":[0,0]

# expedition_data = {
#     "1": {"id":1,"name":"練習航海","time":15,"exp":{"total":{"hq":10,"ship":10},"hourly":{"hq":40,"ship":40}},"yield":{"total":[0,30,0,0],"hourly":[0,120,0,0]},"reward":[None, None],"requirements":{"fs":1,"total":None,"ships":"2XX","drums":None},"consumption":[-3,0]},
#     "2": {"id":2,"name":"長距離練習航海","time":30,"exp":{"total":{"hq":20,"ship":15},"hourly":{"hq":40,"ship":30}},"yield":{"total":[0,100,30,0],"hourly":[0,200,60,0]},"reward":["Bucket", None],"requirements":{"fs":2,"total":None,"ships":"4XX","drums":None},"consumption":[-5,0]},
#     "3": {"id":3,"name":"警備任務","time":20,"exp":{"total":{"hq":30,"ship":30},"hourly":{"hq":90,"ship":90}},"yield":{"total":[30,30,40,0],"hourly":[90,90,120,0]},"reward":[None, None],"requirements":{"fs":3,"total":None,"ships":"3XX","drums":None},"consumption":[-3,-2]},
#     "4": {"id":4,"name":"対潜警戒任務","time":50,"exp":{"total":{"hq":30,"ship":40},"hourly":{"hq":36,"ship":48}},"yield":{"total":[0,60,0,0],"hourly":[0,72,0,0]},"reward":["Bucket", "Small coin box"],"requirements":{"fs":3,"total":None,"ships":"1CL, 2DD OR 1DD, 3DE","drums":None},"consumption":[-5,0]},
#     "5": {"id":5,"name":"海上護衛任務","time":90,"exp":{"total":{"hq":40,"ship":40},"hourly":{"hq":26,"ship":26}},"yield":{"total":[200,200,20,20],"hourly":[133,133,13,13]},"reward":[None, None],"requirements":{"fs":3,"total":None,"ships":"1CL, 2DD, 1XX OR 1DD, 3DE","drums":None},"consumption":[-5,0]},
#     "6": {"id":6,"name":"防空射撃演習","time":40,"exp":{"total":{"hq":30,"ship":50},"hourly":{"hq":45,"ship":75}},"yield":{"total":[0,0,0,80],"hourly":[0,0,0,120]},"reward":["Small coin box", None],"requirements":{"fs":4,"total":None,"ships":"4XX","drums":None},"consumption":[-3,-2]},
#     "7": {"id":7,"name":"観艦式予行","time":60,"exp":{"total":{"hq":60,"ship":120},"hourly":{"hq":60,"ship":120}},"yield":{"total":[0,0,50,30],"hourly":[0,0,50,30]},"reward":["Flamethrower", None],"requirements":{"fs":5,"total":None,"ships":"6XX","drums":None},"consumption":[-5,0]},
#     "8": {"id":8,"name":"観艦式","time":180,"exp":{"total":{"hq":120,"ship":140},"hourly":{"hq":40,"ship":46}},"yield":{"total":[50,100,50,50],"hourly":[16,33,16,16]},"reward":["2x Flamethrower", "DevMat"],"requirements":{"fs":6,"total":None,"ships":"6XX","drums":None},"consumption":[-5,-2]},
#     "9": {"id":9,"name":"タンカー護衛任務","time":240,"exp":{"total":{"hq":60,"ship":60},"hourly":{"hq":15,"ship":15}},"yield":{"total":[350,0,0,0],"hourly":[87,0,0,0]},"reward":["Small coin box", "2x Bucket"],"requirements":{"fs":3,"total":None,"ships":"1CL, 2DD, 1XX","drums":None},"consumption":[-5,0]},
#     "10": {"id":10,"name":"強行偵察任務","time":90,"exp":{"total":{"hq":40,"ship":50},"hourly":{"hq":26,"ship":33}},"yield":{"total":[0,50,0,30],"hourly":[0,33,0,20]},"reward":["Bucket", "Flamethrower"],"requirements":{"fs":3,"total":None,"ships":"2CL, 1XX","drums":None},"consumption":[-3,0]},
#     "11": {"id":11,"name":"ボーキサイト輸送任務","time":300,"exp":{"total":{"hq":40,"ship":40},"hourly":{"hq":8,"ship":8}},"yield":{"total":[0,0,0,250],"hourly":[0,0,0,50]},"reward":["Small coin box", "Bucket"],"requirements":{"fs":6,"total":None,"ships":"2DD, 2XX","drums":None},"consumption":[-5,0]},
#     "12": {"id":12,"name":"資源輸送任務","time":480,"exp":{"total":{"hq":60,"ship":50},"hourly":{"hq":7,"ship":6}},"yield":{"total":[50,250,200,50],"hourly":[6,31,25,6]},"reward":["Medium coin box", "DevMat"],"requirements":{"fs":4,"total":None,"ships":"2DD, 2XX","drums":None},"consumption":[-5,0]},
#     "13": {"id":13,"name":"鼠輸送作戦","time":240,"exp":{"total":{"hq":70,"ship":60},"hourly":{"hq":17,"ship":15}},"yield":{"total":[240,300,0,0],"hourly":[60,75,0,0]},"reward":["2x Bucket", "Small coin box"],"requirements":{"fs":5,"total":None,"ships":"1CL, 4DD, 1XX","drums":None},"consumption":[-5,-4]},
#     "14": {"id":14,"name":"包囲陸戦隊撤収作戦","time":360,"exp":{"total":{"hq":90,"ship":100},"hourly":{"hq":15,"ship":16}},"yield":{"total":[0,240,200,0],"hourly":[0,40,33,0]},"reward":["Bucket", "DevMat"],"requirements":{"fs":6,"total":None,"ships":"1CL, 3DD, 2XX","drums":None},"consumption":[-5,0]},
#     "15": {"id":15,"name":"囮機動部隊支援作戦","time":720,"exp":{"total":{"hq":100,"ship":160},"hourly":{"hq":8,"ship":13}},"yield":{"total":[0,0,300,400],"hourly":[0,0,25,33]},"reward":["Large coin box", "DevMat"],"requirements":{"fs":9,"total":None,"ships":"2CV(L)/AV, 2DD, 2XX","drums":None},"consumption":[-5,-4]},
#     "16": {"id":16,"name":"艦隊決戦援護作戦","time":900,"exp":{"total":{"hq":120,"ship":200},"hourly":{"hq":8,"ship":13}},"yield":{"total":[500,500,200,200],"hourly":[33,33,13,13]},"reward":["2x Flamethrower", "2x DevMat"],"requirements":{"fs":10,"total":None,"ships":"1CL, 2DD, 3XX","drums":None},"consumption":[-5,-4]},
#     "17": {"id":17,"name":"敵地偵察作戦","time":45,"exp":{"total":{"hq":30,"ship":40},"hourly":{"hq":40,"ship":53}},"yield":{"total":[70,70,50,0],"hourly":[93,93,67,0]},"reward":[None, None],"requirements":{"fs":20,"total":None,"ships":"1CL, 3DD, 2XX","drums":None},"consumption":[-3,-4]},
#     "18": {"id":18,"name":"航空機輸送作戦","time":300,"exp":{"total":{"hq":60,"ship":60},"hourly":{"hq":12,"ship":12}},"yield":{"total":[0,0,300,100],"hourly":[0,0,60,20]},"reward":["Bucket", None],"requirements":{"fs":15,"total":None,"ships":"3CV(L)/AV, 2DD, 1XX","drums":None},"consumption":[-5,-2]},
#     "19": {"id":19,"name":"北号作戦","time":360,"exp":{"total":{"hq":60,"ship":70},"hourly":{"hq":10,"ship":11}},"yield":{"total":[400,0,50,30],"hourly":[67,0,8,5]},"reward":["Small coin box", "DevMat"],"requirements":{"fs":20,"total":None,"ships":"2BBV, 2DD, 2XX","drums":None},"consumption":[-5,-4]},
#     "20": {"id":20,"name":"潜水艦哨戒任務","time":120,"exp":{"total":{"hq":40,"ship":50},"hourly":{"hq":20,"ship":25}},"yield":{"total":[0,0,150,0],"hourly":[0,0,75,0]},"reward":["DevMat", "Small coin box"],"requirements":{"fs":1,"total":None,"ships":"1SS(V), 1CL","drums":None},"consumption":[-5,-4]},
#     "21": {"id":21,"name":"北方鼠輸送作戦","time":140,"exp":{"total":{"hq":45,"ship":55},"hourly":{"hq":19,"ship":23}},"yield":{"total":[320,270,0,0],"hourly":[137,116,0,0]},"reward":["Small coin box", None],"requirements":{"fs":15,"total":30,"ships":"1CL, 4DD","drums":"3 total across 3 ships"},"consumption":[-8,-7]},
#     "22": {"id":22,"name":"艦隊演習","time":180,"exp":{"total":{"hq":45,"ship":400},"hourly":{"hq":15,"ship":133}},"yield":{"total":[0,10,0,0],"hourly":[0,3,0,0]},"reward":[None, None],"requirements":{"fs":30,"total":45,"ships":"1CA, 1CL, 2DD, 2XX","drums":None},"consumption":[-8,-7]},
#     "23": {"id":23,"name":"航空戦艦運用演習","time":240,"exp":{"total":{"hq":70,"ship":420},"hourly":{"hq":17,"ship":105}},"yield":{"total":[0,20,0,100],"hourly":[0,5,0,25]},"reward":[None, None],"requirements":{"fs":50,"total":200,"ships":"2BBV, 2DD, 2XX","drums":None},"consumption":[-8,-8]},
#     "24": {"id":24,"name":"北方航路海上護衛","time":500,"exp":{"total":{"hq":65,"ship":80},"hourly":{"hq":7.8,"ship":9.6}},"yield":{"total":[500,0,0,150],"hourly":[60,0,0,18]},"reward":["2x DevMat", "Bucket"],"requirements":{"fs":50,"total":200,"ships":"___1CL___, 4DD, 1XX","drums":"None, but drums increase GS chance"},"consumption":[-9,-6]},
#     "25": {"id":25,"name":"通商破壊作戦","time":2400,"exp":{"total":{"hq":80,"ship":180},"hourly":{"hq":2,"ship":4}},"yield":{"total":[900,0,500,0],"hourly":[23,0,13,0]},"reward":[None, None],"requirements":{"fs":25,"total":None,"ships":"2CA, 2DD","drums":None},"consumption":[-5,-8]},
#     "26": {"id":26,"name":"敵母港空襲作戦","time":4800,"exp":{"total":{"hq":150,"ship":200},"hourly":{"hq":1.87,"ship":2.5}},"yield":{"total":[0,0,0,900],"hourly":[0,0,0,11.25]},"reward":["3x Bucket", None],"requirements":{"fs":30,"total":None,"ships":"1CV(L)/AV, 1CL, 2DD","drums":None},"consumption":[-8,-8]},
#     "27": {"id":27,"name":"潜水艦通商破壊作戦","time":1200,"exp":{"total":{"hq":80,"ship":60},"hourly":{"hq":4,"ship":3}},"yield":{"total":[0,0,800,0],"hourly":[0,0,40,0]},"reward":["DevMat", "2x Small coin box"],"requirements":{"fs":1,"total":None,"ships":"2SS(V)","drums":None},"consumption":[-8,-8]},
#     "28": {"id":28,"name":"西方海域封鎖作戦","time":1500,"exp":{"total":{"hq":100,"ship":140},"hourly":{"hq":4,"ship":5}},"yield":{"total":[0,0,900,350],"hourly":[0,0,36,14]},"reward":["2x DevMat", "Medium coin box"],"requirements":{"fs":30,"total":None,"ships":"3SS(V)","drums":None},"consumption":[-8,-8]},
#     "29": {"id":29,"name":"潜水艦派遣演習","time":1440,"exp":{"total":{"hq":100,"ship":100},"hourly":{"hq":4,"ship":4}},"yield":{"total":[0,0,0,100],"hourly":[0,0,0,4]},"reward":["DevMat", "Small coin box"],"requirements":{"fs":50,"total":None,"ships":"3SS(V)","drums":None},"consumption":[-9,-4]},
#     "30": {"id":30,"name":"潜水艦派遣作戦","time":2880,"exp":{"total":{"hq":100,"ship":150},"hourly":{"hq":2,"ship":3}},"yield":{"total":[0,0,0,100],"hourly":[0,0,0,2]},"reward":["3x DevMat", None],"requirements":{"fs":55,"total":None,"ships":"4SS(V)","drums":None},"consumption":[-9,-7]},
#     "31": {"id":31,"name":"海外艦との接触","time":120,"exp":{"total":{"hq":50,"ship":50},"hourly":{"hq":25,"ship":25}},"yield":{"total":[0,30,0,0],"hourly":[0,15,0,0]},"reward":["Small coin box", None],"requirements":{"fs":60,"total":200,"ships":"4SS(V)","drums":None},"consumption":[-5,0]},
#     "32": {"id":32,"name":"遠洋練習航海 (CT Exped)","time":1440,"exp":{"total":{"hq":300,"ship":"Varies"},"hourly":{"hq":12.5,"ship":"Varies"}},"yield":{"total":[50,50,50,50],"hourly":[2,2,2,2]},"reward":["Large coin box", "3x DevMat"],"requirements":{"fs":5,"total":None,"ships":"___1CT___, 2DD, 3XX","drums":None},"consumption":[-9,-3]},
#     "33": {"id":33,"name":"前衛支援任務 (5-X Node Support)","time":15,"exp":{"total":{"hq":"N/A","ship":"N/A"},"hourly":{"hq":"N/A","ship":"N/A"}},"yield":{"total":[0],"hourly":[0]},"reward":["N/A", "N/A"],"requirements":{"fs":"N/A","total":"N/A","ships":"Support setups","drums":"N/A"},"consumption":[0,0]},
#     "34": {"id":34,"name":"艦隊決戦支援任務 (5-X Boss Support)","time":30,"exp":{"total":{"hq":"N/A","ship":"N/A"},"hourly":{"hq":"N/A","ship":"N/A"}},"yield":{"total":[0],"hourly":[0]},"reward":["N/A", "N/A"],"requirements":{"fs":"N/A","total":"N/A","ships":"Support setups","drums":"N/A"},"consumption":[0,0]},
#     "35": {"id":35,"name":"ＭＯ作戦","time":420,"exp":{"total":{"hq":100,"ship":100},"hourly":{"hq":14,"ship":14}},"yield":{"total":[0,0,240,280],"hourly":[0,0,34,40]},"reward":["2x Small coin box", "DevMat"],"requirements":{"fs":40,"total":None,"ships":"2CV(L)/AV, 1CA, 1DD, 2XX","drums":None},"consumption":[-8,-8]},
#     "36": {"id":36,"name":"水上機基地建設","time":540,"exp":{"total":{"hq":100,"ship":100},"hourly":{"hq":11,"ship":11}},"yield":{"total":[480,0,200,200],"hourly":[53,0,22,22]},"reward":["2x Medium coin box", "Bucket"],"requirements":{"fs":30,"total":None,"ships":"2AV, 1CL, 1DD, 2XX","drums":None},"consumption":[-8,-8]},
#     "37": {"id":37,"name":"東京急行","time":165,"exp":{"total":{"hq":50,"ship":65},"hourly":{"hq":18,"ship":23}},"yield":{"total":[0,380,270,0],"hourly":[0,138,98,0]},"reward":["Small coin box", None],"requirements":{"fs":50,"total":200,"ships":"1CL, 5DD","drums":"4 total across 3 ships"},"consumption":[-8,-8]},
#     "38": {"id":38,"name":"東京急行(弐)","time":175,"exp":{"total":{"hq":100,"ship":70},"hourly":{"hq":34,"ship":24}},"yield":{"total":[420,0,200,0],"hourly":[144,0,69,0]},"reward":["Small coin box", None],"requirements":{"fs":65,"total":240,"ships":"5DD, 1XX","drums":"8 total across 4 ships"},"consumption":[-8,-8]},
#     "39": {"id":39,"name":"遠洋潜水艦作戦","time":1800,"exp":{"total":{"hq":130,"ship":320},"hourly":{"hq":4,"ship":11}},"yield":{"total":[0,0,300,0],"hourly":[0,0,10,0]},"reward":["2x Bucket", "Medium coin box"],"requirements":{"fs":3,"total":180,"ships":"1AS, 4SS","drums":None},"consumption":[-9,-9]},
#     "40": {"id":40,"name":"水上機前線輸送","time":410,"exp":{"total":{"hq":60,"ship":70},"hourly":{"hq":8.9,"ship":10.2}},"yield":{"total":[300,300,0,100],"hourly":[44,44,0,15]},"reward":["3x Small coin box", "Bucket"],"requirements":{"fs":25,"total":150,"ships":"___1CL___, 2AV, 2DD, 1XX","drums":"None, but drums increase GS chance"},"consumption":[-8,-7]},
#     "A1": {"id":"A1", "name":"兵站強化任務","time":25,"exp":{"total":{"hq":15,"ship":10},"hourly":{"hq":36,"ship":24}},"yield":{"total":[45,45,0,0],"hourly":[108,108,0,0]},"reward":[None, None],"requirements":{"fs":5,"total":10,"ships":"3DD/DE, 1XX","drums":"None"},"consumption":[-3.5,0]}
# }

# with shelve.open("db\\expedition_db\\exped_db", "c") as shelf:
#     for exped in expedition_data:
#         shelf[exped] = expedition_data[exped]

# dad_jokes = [
#     "Did you hear about the restaurant on the moon? Great food, no atmosphere.",
#     "What do you call a fake noodle? An Impasta.",
#     "How many apples grow on a tree? All of them.",
#     "Want to hear a joke about paper? Nevermind it's tearable.",
#     "I just watched a program about beavers. It was the best dam program I've ever seen.",
#     "Why did the coffee file a police report? It got mugged.",
#     "How does a penguin build it's house? Igloos it together.",
#     "Dad, did you get a haircut? No I got them all cut.",
#     "What do you call a Mexican who has lost his car? Carlos.",
#     "Dad, can you put my shoes on? No, I don't think they'll fit me.",
#     "Why did the scarecrow win an award? Because he was outstanding in his field.",
#     "Why don't skeletons ever go trick or treating? Because they have no body to go with.",
#     "Ill call you later. Don't call me later, call me Dad.",
#     "What do you call an elephant that doesn't matter? An irrelephant",
#     "Want to hear a joke about construction? I'm still working on it.",
#     "What do you call cheese that isn't yours? Nacho Cheese.",
#     "Why couldn't the bicycle stand up by itself? It was two tired.",
#     "What did the grape do when he got stepped on? He let out a little wine.",
#     "I wouldn't buy anything with velcro. It's a total rip-off.",
#     "The shovel was a ground-breaking invention.",
#     "Dad, can you put the cat out? I didn't know it was on fire.",
#     "This graveyard looks overcrowded. People must be dying to get in there.",
#     'Whenever the cashier at the grocery store asks my dad if he would like the milk in a bag he replies, "No, just leave it in the carton!"',
#     "5/4 of people admit that they’re bad with fractions.",
#     'Two goldfish are in a tank. One says to the other, "do you know how to drive this thing?"',
#     "What do you call a man with a rubber toe? Roberto.",
#     "What do you call a fat psychic? A four-chin teller.",
#     "I would avoid the sushi if I was you. It’s a little fishy.",
#     "To the man in the wheelchair that stole my camouflage jacket... You can hide but you can't run.",
#     "The rotation of earth really makes my day.",
#     "I thought about going on an all-almond diet. But that's just nuts",
#     "What's brown and sticky? A stick.",
#     "I’ve never gone to a gun range before. I decided to give it a shot!",
#     "Why do you never see elephants hiding in trees? Because they're so good at it.",
#     "Did you hear about the kidnapping at school? It's fine, he woke up.",
#     "A furniture store keeps calling me. All I wanted was one night stand.",
#     "I used to work in a shoe recycling shop. It was sole destroying.",
#     "Did I tell you the time I fell in love during a backflip? I was heels over head.",
#     "I don’t play soccer because I enjoy the sport. I’m just doing it for kicks.",
#     "People don’t like having to bend over to get their drinks. We really need to raise the bar.",
# ]

# with open("dad_jokes.pickle", "wb") as f:
#     pickle.dump(dad_jokes, f)

# # GACHA
# # early fall 2018 event
# nelson_gacha = {
#     "ship" : ["Arashio", "Kuroshio", "Oboro", "Shigure", "Kisaragi", "Mikazuki", "Nagatsuki", "Ushio", "Nenohi", "Mochizuki", "Murasame", "Inazuma", "Arare", "Satsuki", "Murakumo", "Fumizuki", "Michishio", "Akebono", "Hatsushimo", "Kasumi", "Kikuzuki", "Ooshio", "Yuudachi", "Shikinami", "Samidare", "Ikazuchi", "Sazanami", "Shiranui", "Wakaba", "Hibiki", "Warspite", "Hatsuzuki", "Ark Royal", "Hagikaze", "Fujinami", "Graf Zeppelin", "Mizuho", "Prinz Eugen", "Hiei", "Kongou", "Kirishima", "Yahagi", "Sakawa", "Yamakaze", "Haruna", "Shirayuki", "Fubuki", "Hatsuyuki", "Natori", "Ayanami", "Jintsuu", "Kiso", "Isonami", "Miyuki", "Isuzu", "Kagerou", "Akatsuki", "Yura", "Tama", "Hatsuharu", "Asashio", "Mutsuki", "Shiratsuyu", "Suzukaze", "Asashimo", "Gotland", "Hiryuu", "Uzuki", "Hyuuga", "Kumano", "Souryuu", "Yamashiro", "Ooi", "Kiyoshimo", "Hayashimo", "Fusou", "Yayoi", "Noshiro", "Myoukou", "Akagi", "Kaga", "Takao", "Kinugasa", "Bismarck", "Suzuya", "Tone", "Ise", "Chikuma", "Atago", "Mogami", "Kitakami", "Arashi", "Nagato", "Mutsu", "Naka"],
#     "count" : [2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 7, 7, 7, 7, 9, 10, 11, 579, 712, 768, 812, 929, 1288, 1426, 1427, 1435, 1440, 1461, 1463, 1477, 1487, 1489, 1698, 1702, 1707, 1721, 1725, 1727, 1730, 1745, 1746, 1748, 1751, 1752, 1768, 1770, 1781, 1783, 1787, 1791, 1812, 2254, 2779, 3093, 3107, 3115, 3139, 3151, 3167, 3174, 3177, 3203, 3205, 3206, 3213, 3216, 3218, 3219, 3231, 3233, 3234, 3235, 3243, 3246, 3250, 3253, 3254, 3308, 3313, 4702, 6209, 9740]
# }

# with open(Path.gacha_folder + "\\nelson_gacha.pickle", "wb") as f:
#     pickle.dump(nelson_gacha, f)
