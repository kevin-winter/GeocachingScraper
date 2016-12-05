import numpy as np
import urllib.request
import json
from bs4 import BeautifulSoup as soup
from pprint import pprint

from Cache import Cache
from User import User
from Commented import Commented
from Utils import findExisting, splitLatLon, persist


def getURLOpener():
    opener = urllib.request.build_opener()
    opener.addheaders.append(('Cookie', 'ASP.NET_SessionId=yphm2zvucctw2mmwv0yw54rw; __qca=P0-1863792981-1474380714775; __RequestVerificationToken=UtV4MO5DrnR_B4BVQfo_4ld-gRpfpeHj2lLcpSszxszxG5di9-9rSCl7aeFMABF7GkY_i1ZbQ0wnmdSJaOD8IHI0fqQ1; ReferringAccountGuid=; SocialMediaAccount={"FirstName":null,"LastName":null,"SuggestedUsername":null}; _gat=1; gspkauth=FiXMYJr6L_F8T5enwxjSn8K4bZP3fA3F_XRwew4R9quQ_1jODUQbeKjGqYOev41X8SRHNuTpJr1ftUQBZawsoTaXFD4qPquCD0OVBWzr_Bz5QO0RqGkA6Omhh8cP7PdmLlfpmksccEKxgK-ofOW-CLGTa96yE1LnirLVbhjRs0A1; Culture=en-US; _ga=GA1.2.1257306678.1474380714'))
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
            batch = [row['data-id'] for row in soup(html, 'lxml').find_all("tr")]
            if batch == []: break
            ids.extend(batch)
            counter += 50
        print(batch)

    for id in ids:
        crawlSingleLocation(id)


def crawlSingleLocation(id):
    url = 'https://www.geocaching.com/geocache/' + id
    opener = getURLOpener()

    with opener.open(url) as response:
        bs = soup(response.read().decode('utf-8'), 'lxml')
        userTokenIndex = int(str(bs).find("userToken = '") + 13)
        userToken = str(bs)[userTokenIndex : userTokenIndex + 167]

        cache = Cache()
        cache.id = id
        try:
            cache.name = bs.find(id="ctl00_ContentBody_CacheName").string
            cache.difficulty = bs.find(id="ctl00_ContentBody_uxLegendScale").img['alt'].split()[0]
            cache.terrain = bs.find(id="ctl00_ContentBody_Localize12").img['alt'].split()[0]
            cache.size = bs.find(id="ctl00_ContentBody_size").img['alt'].split()[1]
            lat, lon = splitLatLon(bs.find(id="uxLatLon").string)
            cache.lat = lat
            cache.lon = lon
            cache.creator = bs.find(id="ctl00_ContentBody_mcd1").a.string.split(',')[0]
        except:
            print("Error parsing fields of cache with ID {}".format(id))

        try:
            getUsers(userToken, cache)
        except:
            print("Error parsing users of cache with ID {}".format(id))


def getUsers(token, cache):
    url = 'https://www.geocaching.com/seek/geocache.logbook?tkn=' + token + '&idx='
    opener = getURLOpener()
    counter = 1
    users = []
    while True:
        with opener.open(url + str(counter)) as response:
            tempUsers = json.loads(response.read().decode('utf-8'))['data']
            if tempUsers == []:
                break
            #users.extend(tempUsers)
            counter += 1

            for u in tempUsers:
                try:
                    user = findExisting("User", u["UserName"])
                    if user is None:
                        user = User()
                        user.username = u["UserName"]
                        #user.AccountGuid = u["AccountGuid"]
                        #user.AccountID = u["AccountID"]
                        #user.Email = u["Email"]
                        user.MembershipLevel = u["MembershipLevel"]
                        user.GeocacheFindCount = u["GeocacheFindCount"]
                        user.GeocacheHideCount = u["GeocacheHideCount"]

                    comment = Commented(user.__ogm__.node, cache.__ogm__.node,
                        Visited = u["Visited"],
                        #ChallengesCompleted = u["ChallengesCompleted"],
                        #LogGuid = u["LogGuid"],
                        #LogID = u["LogID"],
                        #LogText = u["LogText"],
                        LogType = u["LogType"])

                    persist(user, cache, comment)
                    #pprint(comment)
                except:
                    print("Error parsing user of cache with ID {}".format(id))
    print(cache.name, counter*10, "Users")


searchGeoCaching("graz")
#crawlSingleLocation('GC2DAHE')