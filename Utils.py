from py2neo import Graph
from Cache import Cache
from User import User
from Commented import Commented

graph = None


def getGraph():
    global graph
    if graph is None:
        try:
            graph = Graph(host="localhost", password="neo")
        except:
            print("Connection to Neo4jDB failed")
    return graph


def persist(*graphObjects):
    g = getGraph()
    if g is not None:
        t = g.begin()
        for go in graphObjects:
            t.create(go)
        t.commit()


def findExisting(type, key):
    g = getGraph()
    if g is not None:
        if type == "User":
            return User.select(g, key).first()
        elif type == "Cache":
            return Cache.select(g, key).first()


def splitLatLon(location):
    direction = {'N': 1, 'S': -1, 'E': 1, 'W': -1}
    l = location.replace('°', '').split(' ')
    lat = direction[l[0]] * (int(l[1]) + float(l[2]) / 60)
    lon = direction[l[3]] * (int(l[4]) + float(l[5]) / 60)
    return lat, lon