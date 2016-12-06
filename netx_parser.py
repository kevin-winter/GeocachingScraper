import networkx as nx
import numpy as np
import pandas as pd
import json
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.io.img_tiles import MapQuestOSM
from sqlalchemy import create_engine
import geopy

engine = create_engine('mysql+pymysql://root:root@localhost/db')

def getUserDf():
    return pd.read_sql_table("User", con=engine)

def getCacheDf():
    return pd.read_sql_table("Cache", con=engine)

def getAll():
    return pd.read_sql_query('''
      select u.username as username, c.lat as lat, c.lon as lon
      from db.User u
      join db.Commented co on u.accountid = co.user
      join db.Cache c on co.cache = c.id
      ''', con=engine)

df = getAll()
print(np.median(df.lat), np.median(df.lon))
