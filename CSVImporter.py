import pandas as pd
import networkx as nx
import numpy as np
import networkx.algorithms.bipartite as bp
import matplotlib.pyplot as plt

#match (u:User)-[r]-(c:Cache) return c.name, u.username
df = pd.read_csv("C:/Users/kevin/Downloads/edges.csv", delimiter=',')

g = nx.Graph()
g.add_nodes_from(df["c.name"].unique(), bipartite=0)
g.add_nodes_from(df["u.username"].unique(), bipartite=1)
[g.add_edge(row["c.name"], row["u.username"]) for i, row in df.iterrows()]

u,c = bp.sets(g)
unet = bp.projected_graph(g, u)
cnet = bp.projected_graph(g, c)

d = list(unet.degree().values())

plt.hist(d,50, normed=True)
plt.xlabel('Degree k (# of Users)')
plt.ylabel('Fraction $p_k$ of vertices of degree k')
plt.title(r'Cache Degree Distribution on log-scale')

plt.yscale('log')
plt.xscale('log')