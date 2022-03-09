from bs4 import BeautifulSoup
import requests
import json

# tahtsin andmed objektidesse panna, siis saab JSON-i hiljem ühe reaga
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
# kõik kuni mahladeni on OK
for pealkiri in pealkirjad[:3]:
    toidud = pealkiri.next_sibling
    toidulist = []
    for toit in toidud:
        detailid = toit.find_all("h2")
        t = Toit(detailid[0].contents[0], detailid[0].span.text.strip("€"), detailid[0].small.text)
        toidulist.append(t)
    m = Grupp(pealkiri.text, toidulist)
    grupilist.append(m)

# mahladega eraldi jamamine, sest ma ei viitsinud enam
toidud = pealkirjad[3].next_sibling
for toit in toidud:
    joogid = toit.find_all("li")
    toidulist = []
    for jook in joogid:
        t = Toit(jook.h2.contents[0], jook.h2.span.text.strip("€"), "")
        toidulist.append(t)
    m = Grupp(pealkirjad[3].text, toidulist)
    grupilist.append(m)

def obj_dict(obj):
    return obj.__dict__

# kuna mul objektides kõik, siis JSON tehakse mugavalt ühe reaga
json_string = json.dumps(grupilist, default=obj_dict, indent=4)

fail = open("menu.json", "w", encoding="utf8")
fail.write(json_string)
fail.close()