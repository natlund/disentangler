#!usr/bin/python

# Ideas for an algorithm to minimize edge crossings in a graph (network)

import networkx as nx
import math
from matplotlib import pyplot as plt
from layout_generators import *
from graph_geometry import *
from swappers import *


def test_layouts():
    G =nx.gnm_random_graph(10,15)

    rand = [nx.random_layout(G)]
    circ = [nx.circular_layout(G)]
    #shell = [nx.shell_layout(G)] #same as circular layout...
    spectral = [nx.spectral_layout(G)]
    tripod = [tripod_layout(G)]

    layouts = [rand,circ,spectral, tripod]
    regimes = ["random","circular","spectral", "tripod"]

    for layout in layouts:
        layout.append(nx.spring_layout(G,2,layout[0]))
        layout.append(iterate_swaps(G,layout[0]))
        layout.append(nx.spring_layout(G,2,layout[2]))
        layout.append(greedy_swapper(G,layout[0]))

    # Now have list of lists... Find lengths of edgecrossings...

    num_crossings = []
    for layout in layouts:
        for sublayout in layout:
            num_crossings.append(count_crosses(G,sublayout))

    names = []
    for regime in regimes:
        names.append(regime)
        names.append(regime + "-spring")
        names.append(regime + "-swap")
        names.append(regime + "-swap-spr")
        names.append(regime + "-greedy")

    return G, layouts, names, num_crossings


def test_and_plot_layouts():

    print "Generating random graph...\n"

    G, layouts, names, num_crossings = test_layouts()

    print "*******" * 10


    for name, num in zip(names,num_crossings):
        print "Number of edge crossings for {} layout: {}".format(name,num)

    for layout in layouts:
        for sublayout in layout:
            nx.draw(G,sublayout)
            plt.show()

def montecarlo_layout_test():

    #total_crosses = [0,0,0,0,0,0,0,0,0,0,0,0]
    G, layouts, names, total_crosses = test_layouts()

    for i in range(9):
        G, layouts, names, num_crosses = test_layouts()
        total_crosses = [ti + ni for ti, ni in zip(total_crosses,num_crosses)]


    print "Total crosses:"
    for name, num in zip(names,total_crosses):
        print "Total crosses for {} regime: {}".format(name,num)


    plt.bar(range(1,len(names)+1),total_crosses)
    plt.show()




########################################################################

#G, layouts, names, num_crossings = test_layouts()
#print layouts, names, num_crossings

#test_and_plot_layouts()

# Good.  Not sure if coincidence is truly detected - spectral layout
# seems to have overlapping nodes, in the plot at least.

#montecarlo_layout_test()


if __name__ == "__main__":
    G = nx.gnm_random_graph(10,17)
    print G.nodes()
    print "Need to sort by degree.  Put highest degree in center of triangle."
    pos = tripod_layout(G)
    nx.draw(G,pos)
    plt.show()



#~ print "As a starting layout, 'spectral' layout is 2 - 8 times better than"
#~ print "'random' layouts, and up to 10 times better than 'circular' layouts."
#~ print "'spectral-swap' is 3 - 10 times better again."
#~ print "Need to develop spring force layout algorithm that won't allow"
#~ print "a new edge cross to occur, then apply it to 'spectral-swap'.\n"
#~
#~ print "Spring algorithms are all very similar, regardless of starting layout."
#~ print "Spring algorithm also tends to makes any swapped layout worse."
#~ print "TO DO: Try swapping AFTER spring algorithm."
