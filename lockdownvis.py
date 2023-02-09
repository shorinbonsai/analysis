from graphviz import Graph
import sys
import os
import random
from numpy.random import randint
from numpy.random import rand
import copy

from math import exp, log
import matplotlib.pyplot
from PIL import Image, ImageTk
from graphviz import Graph
from statistics import mean

outp = "./Output/"
lower_better = True
alpha = 0.3
shutdown = 3

def infected(sick: int):
    beta = 1 - exp(sick * log(1 - alpha))
    if random.random() < beta:
        return True
    return False

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

def make_adj_lists2(inp: str) -> list[list[int]]:
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

def main():
    random.seed(171391)
    p0 = 0
    global shutdown_percent
    global reopen_percent
    graph_inp = "256graphbest2.dat"
    lock = "lockdown_graph7.dat"
    graph_orig = make_adj_lists(graph_inp)
    lockdown_graph = make_adj_lists2(lock)
    node_numb = len(graph_orig)

    shutdown_percent = 0.05
    reopen_percent = 0.02

    log, score, lockstep, restep = fitness_reopen(graph_orig,node_numb, p0,lockdown_graph)
    print(log)
    pass

def fitness_reopen(adj_lists: list[int], nodes: int, p0, remove_list: list[int] = []):
    temp_list = copy.deepcopy(adj_lists)
    tmp_removed = copy.deepcopy(remove_list)
    n_state = [0 for _ in range(nodes)]  # susceptible
    n_state[p0] = 1
    epi_log = [[p0]]
    num_infected = 1
    ttl_infected = 0
    time_step = 0
    have_locked_down = False
    have_reopened = False
    lockdown_step = 0
    reopen_step = 128
    length = 0
    while num_infected > 0 and time_step < nodes:
        current_infected = num_infected/nodes
        if current_infected >= shutdown_percent and have_locked_down == False:
            temp_list = tmp_removed
            have_locked_down = True
            lockdown_step = time_step

        inf_neighbours = [0 for _ in range(nodes)]

        # if threshold met then restore initial contact graph
        current_infected = num_infected/nodes
        if current_infected < reopen_percent and have_locked_down == True and have_reopened == False:
            temp_list = copy.deepcopy(adj_lists)
            reopen_step = time_step
            have_reopened = True

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
                pass
            elif n_state[n] == 3:
                n_state[n] = 1
                num_infected += 1
                new_inf.append(n)
                pass
            #####ADD SIRRRS HERE  
            elif n_state[n] == 2:
                n_state[n] = 4
            elif n_state[n] == 4:
                n_state[n] = 5
            elif n_state[n] == 5:
                n_state[n] = 0
        epi_log.append(new_inf)
        length += 1
        time_step += 1
        pass
    return epi_log, ttl_infected, lockdown_step, reopen_step



if __name__ == "__main__":
    main()