from graphviz import Graph
import sys
import os
import random
from numpy.random import randint
from numpy.random import rand
import copy

from math import exp, log
import matplotlib.pyplot
# from PIL import Image, ImageTk
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

def edge_list(filename):
    el = []
    with open(filename) as f:
        lines = f.readlines()
        lines.__delitem__(0)
        for from_node, line in enumerate(lines):
            line = line.rstrip()
            line = line.split(" ")
            for to_node in line:
                if to_node != '':
                    # if [from_node, int(to_node)] not in el:
                    # if [int(to_node), from_node] not in el:
                    el.append([from_node, int(to_node)])
                    # pass
                    # pass
                    pass
                pass
            pass
        pass
    edge_lists = []
    edge_counts = []
    for d in el:
        if d not in edge_lists:
            edge_lists.append(d)
            edge_counts.append(el.count(d))
            pass
        pass

    return edge_lists, edge_counts

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

def high_low_deg(el: list, verts: int):
    deg = [int(0) for _ in range(verts)]
    low_deg = []
    high_deg = []
    for ed in el:
        deg[ed[0]] += 1
        deg[ed[1]] += 1
        pass
    max = 0
    for idx, deg in enumerate(deg):
        if deg > max:
            max = deg
            pass
        if deg > 20:
            high_deg.append(idx)
            pass
        elif deg > 10:
            low_deg.append(idx)
            pass
        pass
    print("Max: " + str(max))
    return low_deg, high_deg

def make_graph(el: list, ec: list, low_deg: list, high_deg: list, out_file: str, verts: int, p0: int, lock: int, log: list):
    g = Graph(engine='sfdp')
    e_cout = 0

    g.graph_attr.update(dpi='1000', size="10,10", outputorder='edgesfirst', overlap='false', splines='true')

    g.node_attr.update(color='black', shape='point', width='0.02', height='0.02')

    recovered = []
    for idx, i in enumerate(log):
        if idx < lock:
            for j in log[idx]:
                recovered.append(j)

    for i in recovered:
        g.node(str(i), label=str(i), color='orange', width='0.03', height='0.03')

    for i in log[lock]:
        g.node(str(i), label=str(i), color='green', width='0.03', height='0.03')

    g.edge_attr.update(color='black', penwidth='0.5')
    for n in range(verts):
        if n == p0:
            if n in low_deg:
                g.node(str(n), label=str(n), color='red', width='0.03', height='0.03')
                pass
            elif n in high_deg:
                g.node(str(n), label=str(n), color='red', width='0.04', height='0.04')
                pass
            else:
                g.node(str(n), label=str(n), color='red')
                pass
        elif n in low_deg:
            g.node(str(n), label=str(n), width='0.03', height='0.03')
        elif n in high_deg:
            g.node(str(n), label=str(n), width='0.04', height='0.04')
        else:
            g.node(str(n), label=str(n))
        pass

    ew_count = 0
    counts = [0 for _ in range(5)]
    for idx, d in enumerate(el):
        if d[0] < d[1]:
            if ec[idx] == 1:
                g.edge(str(d[0]), str(d[1]), color='black')
                pass
            elif ec[idx] == 2:
                g.edge(str(d[0]), str(d[1]), color='purple')
                pass
            elif ec[idx] == 3:
                g.edge(str(d[0]), str(d[1]), color='blue')
                pass
            elif ec[idx] == 4:
                g.edge(str(d[0]), str(d[1]), color='orange')
                pass
            else:
                g.edge(str(d[0]), str(d[1]), color='red')
                pass

            # g.edge(str(d[0]), str(d[1]), penwidth=str(pw * ec[idx]))
            e_cout += 1
            ew_count += ec[idx]
            counts[ec[idx] - 1] += 1
            pass
        pass

    print("Edges: " + str(e_cout))
    print("Total Weights: " + str(ew_count))
    print(counts)
    g.render(filename=out_file, directory=outp, cleanup=True, format='png')
    g.save(filename=out_file, directory=outp)
    pass


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
    # random.seed(171391)
    p0 = 132
    global shutdown_percent
    global reopen_percent
    graph_inp = "256graphbest2.dat"
    lock = "lockdown_graph7.dat"
    graph_orig = make_adj_lists(graph_inp)
    lockdown_graph = make_adj_lists2(lock)
    edge1, ec = edge_list(graph_inp)
    edge2 = get_edge_list(graph_inp)
    node_numb = len(graph_orig)

    shutdown_percent = 0.05
    reopen_percent = 0.02

    log, score, lockstep, restep = fitness_reopen(graph_orig,node_numb, p0,lockdown_graph)
    low_deg, high_deg = high_low_deg(edge1, 256)
    make_graph(edge1, ec, low_deg, high_deg, "testgraph", 256,132, lockstep, log)
    print(log)
    pass

def fitness_reopen(adj_lists: list[list[int]], nodes: int, p0, remove_list: list[list[int]] = []):
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
