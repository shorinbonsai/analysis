import copy
# import operator
# import math
import random
import sys
import numpy as np
import csv
import os
# import pandas as pd
from math import exp, log
# import matplotlib.pyplot
# from PIL import Image, ImageTk
# from graphviz import Graph
from statistics import mean

# from numpy.random import randint
# from numpy.random import rand


alpha = 0.3
shutdown = 3


def infected(sick: int):
    beta = 1 - exp(sick * log(1 - alpha))
    if random.random() < beta:
        return True
    return False


def make_adj_listsO(inp: str):
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


def main():
    #random.seed(1431423)
    p0 = 0
    graph_inp = "graphForJames_new.dat"
    graph_orig = make_adj_listsO(graph_inp)
    node_numb = len(graph_orig)
    
    # for dirpath, dirnames, files in os.walk('.'):
    #     for file_name in files:
    #         :
    # graphs,lockdowns, strictness, files  = get_bests("bestofbest.txt")
    pwd = os.getcwd()
    rootdir = pwd.strip().split('/')[-1]
    data = []
    for _ in range(1000):
        log, score, length = fitness_bare(graph_orig,node_numb, p0)
        data.append(length)

    import numpy as np
    import scipy.stats
    def mean_confidence_interval(data, confidence=0.95):
        a = 1.0 * np.array(data)
        n = len(a)
        m, se = np.mean(a), scipy.stats.sem(a)
        h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
        return m, m-h, m+h

    print(mean_confidence_interval(data))

    with open('testTesttest.txt', 'w') as f:
        print(data, file=f)
        print("Avg: " + str(mean(data)), file=f)



    # lockdown_graph = make_adj_lists(files[0])
    # if rootdir == "256g":
    #     p0 = 212
    # elif rootdir == "256g2":
    #     p0 = 132
    # elif rootdir == "256g3":
    #     p0 = 118
    # elif rootdir == "512g":
    #     p0 = 479
    # elif rootdir == "512g2":
    #     p0 = 43
    # elif rootdir == "512g3":
    #     p0 = 479

    # with open(graph_inp + "_nolockdown.csv", mode='w')  as f:
    #     csvwriter = csv.writer(f)
    #     result = []    
    #     for j in range(30):
    #         score = 0
    #         while score <5:
    #             _, score = fitness_bare(graph_orig,node_numb, p0)
    #         result.append(score)
    #         csvwriter.writerow([score])    
    print("test")

    return

def make_adj_lists(inp: str) -> list[list[int]]:
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

def fitness_bare(adj_lists: list[list[int]], nodes: int, p0):
    temp_list = copy.deepcopy(adj_lists)
    n_state = [0 for _ in range(nodes)]  # susceptible
    n_state[p0] = 1
    epi_log = [[p0]]
    num_infected = 1
    ttl_infected = 0
    time_step = 0
    length = 0
    while num_infected > 0 and time_step < nodes:
        current_infected = num_infected/nodes
        inf_neighbours = [0 for _ in range(nodes)]
        current_infected = num_infected/nodes
        for n in range(nodes):
            if n_state[n] == 1:
                for nei in temp_list[n]:
                    inf_neighbours[nei] += 1
        for n in range(nodes):
            if n_state[n] == 0 and inf_neighbours[n] > 0:
                if infected(inf_neighbours[n]):
                    n_state[n] = 3
        ttl_infected += num_infected
        num_infected = 0
        new_inf = []
        for n in range(nodes):
            if n_state[n] == 1:  # infected -> removed
                n_state[n] = 2
            elif n_state[n] == 3:
                n_state[n] = 1
                num_infected += 1
                new_inf.append(n)
        epi_log.append(new_inf)
        length += 1
        time_step += 1
    return epi_log, ttl_infected, length


if __name__ == "__main__":
    main()






            #####ADD SIRRRS HERE  
            # elif n_state[n] == 2:
            #     n_state[n] = 4
            # elif n_state[n] == 4:
            #     n_state[n] = 5
            # elif n_state[n] == 5:
            #     n_state[n] = 0