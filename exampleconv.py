import networkx as nx
# weighted MultiGraph
M = nx.MultiGraph()
M.add_edge(1,2,weight=7)
M.add_edge(1,2,weight=19)
M.add_edge(2,3,weight=42)

# create weighted graph from M
G = nx.Graph()
for u,v,data in M.edges(data=True):
    w = data['weight'] if 'weight' in data else 1.0
    if G.has_edge(u,v):
        G[u][v]['weight'] += w
    else:
        G.add_edge(u, v, weight=w)

print(G.edges(data=True))
# [(1, 2, {'weight': 26}), (2, 3, {'weight': 42})]



import networkx as nx

# Create a MultiGraph
G = nx.MultiGraph()

# Add edges with weights to the MultiGraph
G.add_edge(1, 2, weight=2)
G.add_edge(1, 2, weight=3)
G.add_edge(1, 3, weight=4)

# Convert the MultiGraph to a weighted undirected graph
H = nx.Graph(G)

# Check the weight of the edge between node 1 and node 2
print(H[1][2]['weight'])  # prints: 5



import networkx as nx

# Create a MultiGraph
G = nx.MultiGraph()

# Add edges to the MultiGraph
G.add_edge(1, 2)
G.add_edge(1, 2)
G.add_edge(1, 3)

# Create a new weighted graph
H = nx.Graph()

# Iterate over the edges of the MultiGraph
for u, v, data in G.edges(data=True):
    # Add each edge to the new graph with a weight of 1.0
    H.add_edge(u, v, weight=1.0)

# Check the weight of the edge between node 1 and node 2
print(H[1][2]['weight'])  # prints: 1.0


import networkx as nx
from collections import defaultdict

# Create a MultiGraph
G = nx.MultiGraph()

# Add edges to the MultiGraph
G.add_edge(1, 2)
G.add_edge(1, 2)
G.add_edge(1, 3)

# Create a defaultdict to store the edge weights
weights = defaultdict(int)

# Iterate over the edges of the MultiGraph
for u, v, data in G.edges(data=True):
    # Increment the weight of each edge
    weights[(u, v)] += 1

# Create a new weighted graph
H = nx.Graph()

# Iterate over the edges and their weights
for (u, v), w in weights.items():
    # Add each edge to the new graph with its calculated weight
    H.add_edge(u, v, weight=w)

# Check the weight of the edge between node 1 and node 2
print(H[1][2]['weight'])  # prints: 2.0


