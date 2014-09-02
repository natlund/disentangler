#!usr/bin/python

# Ideas for an algorithm to minimize edge crossings in a graph (network)

# This module generates layouts that attempt to give best potential for
# minimising edge crossings.   Ideally, these layouts will give lowest
# edge crossings after swapping the node positions for enough iterations.
# Equivalently, these layouts attempt to minimise edge crossings for
# a clique.

import networkx as nx
import math
from matplotlib import pyplot as plt


###################################################################################
########## Generators for Nested-Triangle Type Layouts


def tripod_layout(G):
    """Return layout of nested triangles, with vertices aligned
       on straight lines, like the birdseye view of a tripod."""
    pos = {}
    dummy = tripod_coords(len(G.nodes()))#get_next_coord(len(G.nodes() ) )
    for node in G.nodes():
        pos[node] = dummy.next()

    return pos

def get_next_coord(num_nodes):
    count = 0
    newx, newy = 0.0, 0.0
    length = 1.0
    while count < num_nodes:
        yield (newx,newy)
        # Keep 60 degree angles the same, but increase length by 10%
        if count%3 == 0:
            newx = newx + length
        elif count%3 == 1:
            newx = newx - length * 0.5
            newy = newy + length * 0.866
        else:
            newx = newx - length * 0.5
            newy = newy - length * 0.866

        length = length * 1.2
        count += 1

def tripod_coords(num_nodes):
    print "tripod coords"
    count = 0
    while count < num_nodes:
        shell_count = count / 3
        if count % 3 == 0:
            newx = -0.5 - (1.733*shell_count * 0.5)
            newy = -0.289 - (1.733*shell_count * 0.289)
        elif count % 3 == 1:
            newx = 0.5 + (1.733*shell_count * 0.5)
            newy = -0.289 - (1.733*shell_count * 0.289)
        else:
            newx = 0
            newy = 0.577 + (1.733*shell_count * 0.577)

        yield newx, newy
        count += 1


def test_tripod_layout():

    print "Yo", get_next_coord(1)
    dummy = get_next_coord(7)
    print "Coord 1:", dummy.next()
    print "Coord 2:", dummy.next()
    print "Coord 3:", dummy.next()
    print "Coord 4:", dummy.next()
    print "Coord 5:", dummy.next()
    print "Coord 6:", dummy.next()

    G = nx.gnm_random_graph(10,15)
    pos = tripod_layout(G)
    print pos
    nx.draw(G,pos)
    plt.show()


if __name__ == "__main__":
    test_tripod_layout()
