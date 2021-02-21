import discord



class Controller():
    def __init__(self,callsign,controller_name,frequency):
        self.callsign = callsign
        self.controller_name = controller_name
        self.frequency = frequency
    def get_callsign(self):
        return self.callsign
    def get_controller_name(self):
        return self.controller_name
    def get_frequency(self):
        return self.frequency

import requests, time
callsign_prefix = ["EHB", "EHL", "EHR", "EHG", "EHE"]
positions = ["DEL","GND","TWR", "APP", "ARR"]
url="https://data.vatsim.net/vatsim-data.txt"
webhook_url=""
online_cs = []
webhook_url="https://discord.com/api/webhooks/812809969413914634/LWYL2Qdf3l9_fJ_giNDHu17bOAZfxDcbpQZM8BZA_mWg-9p1kifC0HGZErHqfkVrpsO1"
while True:
    try:
        print("Starting...")
        online_2_cs = []
        online_2_obj = []
        r = requests.get(url)
        y = r.text.splitlines()[10:]
        for a in y:
            b = ""
            if a != "":
                b = a.split(":")
            else:
                break
            callsign = b[0]
            for i in callsign_prefix:
                if i == callsign[:3] and callsign[-3:] in positions and callsign != "VCL_CTR":
                    #callsign positive!
                    cid = b[1]
                    controller_name = b[2]
                    frequency = b[4]
                    controller_obj = Controller(callsign,controller_name,frequency)
                    online_2_obj.append(controller_obj)
                    online_2_cs.append(callsign)
        for i in online_2_obj:
            if i.get_callsign() not in online_cs:
                #new online callsign
                online_cs.append(i.get_callsign())
                content = "Hello ! {} is now online on {} frequency {}!".format(i.get_controller_name(),i.get_callsign(),i.get_frequency())
                data = {"username":"ATC is online!","content":content}
                response = requests.post(webhook_url, json=data)
                code = response.status_code
                if code == 204:
                    print("Success! {} {} {}".format(i.get_controller_name(),i.get_callsign(),i.get_frequency()))
                else:
                    print("FUCK")
            time.sleep(5)
        #check for old callsigns
        for i in online_cs:
            if i not in online_2_cs:
                online_cs.remove(i)
                content = "Aww, {} is now offline. See you next time!".format(i)
                data = {"username":"ATC is offline :(","content":content}
                response = requests.post(webhook_url, json=data)
                code = response.status_code
                print("Aww, {} offline".format(i))
        print("All done, now waiting for 3 minutes.")
        time.sleep(180)
    except KeyboardInterrupt:
        break
