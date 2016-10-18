from py2neo.ogm import GraphObject, Related, Property

import Cache
import Commented


class User(GraphObject):
    __primarykey__ = "username"

    username = Property()
    AccountGuid = Property()
    AccountID = Property()
    Email = Property()
    GeocacheFindCount = Property()
    GeocacheHideCount = Property()
    MembershipLevel = Property()

    commentedCaches = Related(Cache, Commented)
    createdCaches = Related(Cache, "CREATED")



