from py2neo.ogm import Property
from py2neo import Relationship

class Commented(Relationship):
    __primarykey__ = "LogGuid"

    LogGuid = Property()
    LogID = Property()
    ChallengesCompleted = Property()
    LogText = Property()
    LogType = Property()
    Visited = Property()
