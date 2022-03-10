from bs4 import BeautifulSoup
import requests
import json

# andmed objektidesse, siis saab JSON-i hiljem ühe reaga
class Grupp:
    def __init__(self, nimetus, toidud):
        self.nimetus = nimetus
        self.toidud = toidud

class Toit:
    def __init__(self, nimetus, hind, lisainfo):
        self.nimetus = nimetus
        self.hind = hind
        self.lisainfo = lisainfo

# url = "https://siseveeb.voco.ee/veebivormid/sookla_menuu"
url = 'http://192.168.22.172/menu-example/'
sisu = requests.get(url).text
doc = BeautifulSoup(sisu, "html.parser")

pealkirjad = doc.find_all("div", {"class": "panel-heading text-center"})

grupilist = []
for pealkiri in pealkirjad:
    toidud = pealkiri.parent.find_all("li")
    toidulist = []
    for toit in toidud:
        detailid = toit.find_all("h2")
        t = Toit(detailid[0].contents[0], detailid[0].span.text.strip("€"), detailid[0].small.text)
        toidulist.append(t)
    m = Grupp(pealkiri.text, toidulist)
    grupilist.append(m)

def obj_dict(obj):
    return obj.__dict__

with open('menu.json', 'w') as f:
    json.dump(grupilist, f, default=obj_dict, indent=4)

