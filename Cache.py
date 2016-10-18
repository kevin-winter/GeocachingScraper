from py2neo.ogm import GraphObject, Related, Property

import User, Commented

class Cache(GraphObject):
    __primarykey__ = "id"

    id = Property()
    name = Property()
    difficulty = Property()
    terrain = Property()
    size = Property()
    location = Property()

    creator = Related(User, "CREATED")
    users = Related(User, Commented)
