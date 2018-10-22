from typing import Dict

import requests as rr
import json
import datetime


def bitfield(n):
    return [int(digit) for digit in bin(n)[2:]]


Airports: Dict[str, str] = {"B": "BIA", "T": "TLN", "N": "NCE"}
datdep = "08/06/2018"
codlign = "TB"
hordep = "21:00"

# Bourg en bresse
lat = "46.20244220000"
lng = "5.189942840000"
# DOLE
lat = "47.106"
lng = "5.436"

dd = (datetime.datetime.strptime(datdep, "%d/%m/%Y").weekday() + 1) % 7

#
# headersData = {}
# request = rr.get("https://airport.api.aero/airport/nearest/"+lat+"/"+lng+"?user_key=3af729ff29ca0c6d959bb5069db4d8b8",headers=headersData)
# data=json.loads(request.content[9:-1],strict=False)
# airport=data["airports"][0]["code"]
Rtitles = []
headersData = {}
request = rr.get(
    "http://free.rome2rio.com/api/1.4/json/Search?key=NrRtUFvJ&oPos=" + lat + "," + lng + "&dName=" + Airports[
        codlign[1]] + "&currency=EUR", headers=headersData)
data = json.loads(request.content, strict=False)
routes = [x for x in data["routes"] if "ly" in x["name"]]
for route in routes:
    print("--------------\n", route["name"])
    Rtitles.append(route["name"])
    segms = [x for x in route["segments"] if x["segmentKind"] == "air"]
    for segm in segms:
        transitDuration = (segm["transitDuration"])
        indicativePrices = (segm["indicativePrices"])
        OutHops = segm["outbound"]
        # RetHops=segm["return"]["hops"]
        for hop in OutHops:
            # print(OutHops)
            hl = len(hop["hops"])
            if hl > 1:
                print("\nVol Avec Escale")
            odbin = bitfield(hop["operatingDays"])
            if len(odbin) > dd:
                if odbin[dd] == 0:
                    print("Départ différé")
            else:
                print("Départ différé")
            print("\n", hop["operatingDays"], odbin, hop["indicativePrices"])
            depTime = hop["hops"][0]["depTime"]
            arrTime = hop["hops"][hl - 1]["arrTime"]
            print(depTime, " ", arrTime)
print(Rtitles)