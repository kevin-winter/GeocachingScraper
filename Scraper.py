import numpy as np
import urllib.request
import json
from bs4 import BeautifulSoup as soup
from pprint import pprint

from py2neo import Graph
import Cache, Commented, User

def fillNeo4jDB():
    graph = Graph(host="localhost")


def splitLatLon(location):
    direction = {'N': 1, 'S': -1, 'E': 1, 'W': -1}
    l = location.replace('°', '').split(' ')
    lat = direction[l[0]] * (int(l[1]) + float(l[2]) / 60)
    lon = direction[l[3]] * (int(l[4]) + float(l[5]) / 60)
    return (lat, lon)


def getURLOpener():
    opener = urllib.request.build_opener()
    opener.addheaders.append(('Cookie', 'ASP.NET_SessionId=yphm2zvucctw2mmwv0yw54rw;'
                                        ' __qca=P0-1863792981-1474380714775;'
                                        ' __RequestVerificationToken=UtV4MO5DrnR_B4BVQfo_4ld-gRpfpeHj2lLcpSszxszxG5di9-9rSCl7aeFMABF7GkY_i1ZbQ0wnmdSJaOD8IHI0fqQ1;'
                                        ' ReferringAccountGuid=; SocialMediaAccount={"FirstName":null,"LastName":null,"SuggestedUsername":null};'
                                        ' gspkauth=jhbvS13ak_S-aJfGZks4BxN30iiHonXWKMI_oz5orfAsPB-jWz-NNWwXovW2u9EMx7IYiG6J7IZ-fYtUCjpHkNqvnX55DnaUeGbmRaOIR2DX_AoOd5l-Dtw870WjpSSfxrVy2AhDdQFvjS8DkAhoJybs_EjM6Hbjm0S4eW3k0S01;'
                                        ' Culture=en-US; _ga=GA1.2.1257306678.1474380714'))
    return opener


def searchGeoCaching(city):
    url = 'https://www.geocaching.com/play/search/more-results' \
          '?selectAll=false&origin=' + city + '&startIndex='
    opener = getURLOpener()

    ids = []
    counter = 0
    while True:
        with opener.open(url + str(counter)) as response:
            html = json.loads(response.read().decode('utf-8'))['HtmlString']
            if html == '': break

            batch = [row['data-id'] for row in soup(html, 'lxml').find_all("tr")]
            ids.extend(batch)
            counter += 50

    for id in ids:
        crawlSingleLocation(id)



def crawlSingleLocation(id):
    url = 'https://www.geocaching.com/geocache/' + id
    opener = getURLOpener()

    with opener.open(url) as response:
        bs = soup(response.read().decode('utf-8'), 'lxml')
        userTokenIndex = int(str(bs).find("userToken = '") + 13)
        userToken = str(bs)[userTokenIndex : userTokenIndex + 167]

        name = bs.find(id="ctl00_ContentBody_CacheName").string
        difficulty = bs.find(id="ctl00_ContentBody_uxLegendScale").img['alt'].split()[0]
        terrain = bs.find(id="ctl00_ContentBody_Localize12").img['alt'].split()[0]
        size = bs.find(id="ctl00_ContentBody_size").img['alt'].split()[1]
        location = splitLatLon(bs.find(id="uxLatLon").string)
        creator = bs.find(id="ctl00_ContentBody_mcd1").a.string.split(',')[0]

        getUsers(userToken)


def getUsers(token):
    url = 'https://www.geocaching.com/seek/geocache.logbook?tkn=' + token + '&idx='
    opener = getURLOpener()
    counter = 1

    users = []
    while True:
        with opener.open(url + str(counter)) as response:
            users = json.loads(response.read().decode('utf-8'))['data']
            if users == '': break

            users.extend(users)
            for user in users:
                pprint(user["UserName"])
            counter += 1
            break

    #pprint(users)

#searchGeoCaching("Vienna")
crawlSingleLocation('GC2DAHE')