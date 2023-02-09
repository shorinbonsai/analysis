from collections import defaultdict
import networkx as nx

import os
import sys
import random

def make_adj_lists(inp: str):
    with open(inp, "r") as f:
        first_line = f.readline()
        nodes = int(first_line.rstrip().split('\t')[0].split(' ')[1])
        adj_lists = [[] for _ in range(nodes)]
        lines = f.readlines()
        for fr, line in enumerate(lines):
            line = line.rstrip()
            line = line.split(' ')
            if len(line) > 0:
                for to in line:
                    if to != '':
                        adj_lists[fr].append(int(to))
    return adj_lists


def make_adj_lists_lock(inp: str) -> list[list[int]]:
    with open(inp, "r") as f:
        first_line = f.readline()
        nodes = first_line.strip()
        nodes = nodes.split(',')
        nodes = nodes[0]
        nodes = nodes.split(': ')
        nodes = int(nodes[1])
        adj_lists = [[] for _ in range(nodes)]
        lines = f.readlines()
        for fr, line in enumerate(lines):
            line = line.rstrip()
            line = line.split(' ')
            if len(line) > 0:
                for to in line:
                    if to != '':
                        adj_lists[fr].append(int(to))

    return adj_lists

def get_edge_list(inp: str):
    with open(inp, "r") as f:
        first_line = f.readline()
        first_line = first_line.strip('\n')
        first_line = first_line.split(' ')
        nodes = int(first_line[0])
        edges = int(first_line[2])
        edg_list = []
        lines = f.readlines()
        
        for fr, line in enumerate(lines):
            line = line.rstrip()
            line = line.split(' ')
            if len(line) > 0:
                for to in line:
                    if to != '' and int(to) > fr:
                        edg_list.append((fr, int(to)))
                        pass
                    pass
                pass
            pass
    return edg_list

def main():
    alphas = [0.7, 0.49, 0.343, 0.2401, 0.16807]
    graph_inp = "256graphbest.dat"
    tmp = get_edge_list(graph_inp)

    M = nx.MultiGraph()
    for i in tmp:
        M.add_edge(i[0], i[1])
    # M = nx.read_adjlist(graph_inp)
    # print(M.edges())

    weights = defaultdict(int)
    # Iterate over the edges of the MultiGraph
    for u, v, data in M.edges(data=True):
        # Increment the weight of each edge
        weights[(u, v)] += 1

    H = nx.Graph()
    for (u, v), w in weights.items():
        # Add each edge to the new graph with its calculated weight
        H.add_edge(u, v, weight=w)

    inverse = nx.Graph()
    standard = nx.Graph()
    for i in H.edges():
        H[i[0]][i[1]]['weight'] = alphas[H[i[0]][i[1]]['weight']-1]

    print("cat")
    pass

if __name__ == "__main__":
    main()