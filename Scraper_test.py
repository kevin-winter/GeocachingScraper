import numpy as np
import urllib.request
import json
from bs4 import BeautifulSoup as soup
from pprint import pprint

from Cache import Cache
from User import User
from Commented import Commented
from py2neo import Relationship
from Utils import findExisting, splitLatLon, persist


def searchGeoCaching(city):
    ids = ["A", "B", "C", "D"]
    for id in ids:
        crawlSingleLocation(id)


def crawlSingleLocation(id):
    cache = Cache()
    cache.id = id
    cache.name = id + "name"
    cache.difficulty = 2
    cache.terrain = 3
    cache.size = 2
    getUsers(cache)


def getUsers(cache):
    users = ["u1","u2","u3","u4","u5"]

    for u in users:
        user = findExisting("User", u)
        if user is None:
            user = User()
            user.username = u + "name"
            user.GeocacheFindCount = 3
            user.GeocacheHideCount = 5


        comment = Commented(user.__ogm__.node, cache.__ogm__.node, visited = "10.10.2000")
        persist(user, cache, comment)
        print(user.username, user.GeocacheFindCount)
        pprint(comment)


searchGeoCaching("Vienna")
#crawlSingleLocation('GC2DAHE')