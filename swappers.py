#!usr/bin/python

# Ideas for an algorithm to minimize edge crossings in a graph (network)

import networkx as nx
import math
from matplotlib import pyplot as plt
from graph_geometry import *

# Algorithms that swap the position of nodes in a given layout,
# to find the positions that mimimise edge crossings.

def find_best_pair_swap(G,start_pos):
    """Given a starting layout, swap positions of all possible
       node pairs, testing number of edge crossings each time.
       Return layout with the pair swap that minimizes edge crossings."""

    best_crossings = count_crosses(G,start_pos)
    best_pos = start_pos.copy()

    swapnode1, swapnode2 = "nothing", "nothing"

# Iterate through all pairs of nodes.
    for i, node1 in enumerate(G.nodes()):
        for node2 in G.nodes()[i+1:]:
            # Start with original start_pos each iteration
            pos = start_pos.copy()
            # Swap positions of the two nodes.
            dummy = pos[node1]
            pos[node1] = pos[node2]
            pos[node2] = dummy

            crossings = count_crosses(G,pos)
            #print "Swapping {} and {} gives {} crossings.".format(node1,node2,crossings)

            if crossings < best_crossings:
                best_crossings = crossings
                print "Swapping {} and {} would reduce crossings to {}".format(node1,node2,crossings)
                best_pos = pos.copy()
                swapnode1, swapnode2 = node1, node2

    print "Checked all pairs, have swapped {} and {}".format(swapnode1,swapnode2)

    return best_pos, best_crossings

def greedy_best_swap(G,start_pos):

    best_crossings = count_crosses(G,start_pos)
    best_pos = start_pos.copy()

    for i, node1 in enumerate(G.nodes()):
        for node2 in G.nodes()[i+1:]:
            # Use new best_pos each iteration
            pos = best_pos.copy()
            # Swap positions of the two nodes.
            dummy = pos[node1]
            pos[node1] = pos[node2]
            pos[node2] = dummy

            crossings = count_crosses(G,pos)
            #print "Swapping {} and {} gives {} crossings.".format(node1,node2,crossings)

            if crossings < best_crossings:
                best_crossings = crossings
                print "Swapped {} and {}, reducing crossings to {}".format(node1,node2,crossings)
                best_pos = pos.copy()

    return best_pos, best_crossings




def iterate_swaps(G, start_pos):
    """Given start position (layout), perform all possible pair swaps,
       remembering which layout minimizes crossings.
       Starting with minimizing layout, again perform all
       possible pair swaps.  Iterate until no further improvement."""

    best_pos = start_pos.copy()

    best_crossings = count_crosses(G,best_pos)
    if best_crossings == 0:
        return best_pos

    for x in range(1,len(G.nodes())):
        print "\nIteration number:",x

        new_pos, new_crossings = find_best_pair_swap(G, best_pos)

        if new_crossings < best_crossings:
            best_pos = new_pos.copy()
            best_crossings = new_crossings
            if best_crossings == 0:
                print "Success!  Zero crossings."
                break

        else:
            print "Dead end!  Progress stuck at {} crossings.".format(best_crossings)
            break

    return best_pos


def greedy_swapper(G,start_pos):

    best_pos = start_pos.copy()

    best_crossings = count_crosses(G,best_pos)
    if best_crossings == 0:
        return best_pos

    for x in range(1,len(G.nodes())):
        print "\nGreedy Iteration number:",x

        new_pos, new_crossings = greedy_best_swap(G, best_pos)
        #new_crossings = count_crosses(G,new_pos)

        if new_crossings < best_crossings:
            best_pos = new_pos.copy()
            best_crossings = new_crossings
            if best_crossings == 0:
                print "Greedy Success!  Zero crossings."
                break

        else:
            print "Greedy Dead end!  Progress stuck at {} crossings.".format(best_crossings)
            break

    return best_pos



def circular_iterate(G, start_pos=None):
    """Given graph G, generate circular layout, swap all pairs
       to find layout that minimizes crossings, repeat for
       new layout until no further improvement.
       I suspect circular layout is the worst place to start!"""
    if start_pos == None: start_pos = nx.circular_layout(G)

    pos = iterate_swaps(G,start_pos)

    return pos

