from py2neo import Graph
from Cache import Cache as GCache
from User import User as GUser

from SQLClasses import *

graph = None
dbType = ""

def getGraph():
    global graph
    if graph is None:
        try:
            graph = Graph(host="localhost", password="neo")
        except:
            print("Connection to Neo4jDB failed")
    return graph



def persist(*objects):

    if dbType == "graph":
        g = getGraph()
        if g is not None:
            t = g.begin()
            for go in objects:
                t.create(go)
            t.commit()
    if dbType == "sql":
        for go in objects:
            go.save()

def findExisting(type, key):

    if dbType == "graph":
        g = getGraph()
        if g is not None:
            if type == "User":
                return GUser.select(g, key).first()
            elif type == "Cache":
                return GCache.select(g, key).first()

    if dbType == "sql":
        if type == "User":
            user = None
            try:
                user = User.get(User.username == key)
            finally:
                return user

        elif type == "Cache":
            cache = None
            try:
                cache = Cache.get(Cache.id == key)
            finally:
                return cache


def splitLatLon(location):
    direction = {'N': 1, 'S': -1, 'E': 1, 'W': -1}
    l = location.replace('°', '').split(' ')
    lat = direction[l[0]] * (int(l[1]) + float(l[2]) / 60)
    lon = direction[l[3]] * (int(l[4]) + float(l[5]) / 60)
    return lat, lon