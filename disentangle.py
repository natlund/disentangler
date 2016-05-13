#!usr/bin/python

import networkx as nx
from montecarlo import run_simulation
from evol_nx_layout import evolve_asexually

"""
This the main file for the disentangler project.

The purpose of the project is to find algorithms to draw a two-dimensional
network graph (of nodes and edges) in a nice way.  That is, with minimal
edge crossings, maximum symmetry, and in general in a clean, easy-to-understand
way.

The disentangler project is a work in progress.  The current state is good,
but not perfect.  For simple cases, a graph layout is produced that has
no edge crossings, no nodes lying stupidly close to edges, and no absurdly
long edges.  But it can still look a bit weird, not quite right.
Experiments continue...

The project holds a lot of dead ends - strategies that were tried
and found not to be fruitful.  Therefore, there is a lot of code that is
essentially dead - it will never be used again, but is kept as a record
of experiments that were done.

The best approach discovered so far is an essentially random approach -
move nodes around at random and see if it makes it better.  This started
out as a genetic algorithm, with sexual reproduction, and a fitness function.
It was discovered that ASEXUAL reproduction gave better results.
An asexual reproduction algorithm ought to be equivalent to some 
kind of Montecarlo algorithm.  

Therefore, the latest learnings have been incorporated into a simple
Montecarlo algorithm.  It behaves the same as the asexual genetic algoritm,
but is vastly simpler, not needing all the genetics framework.
"""

def elegant_layout(G):
    '''
    Given networkx graph G, return a nice elegant layout.
    '''
    seed = nx.spring_layout(G)
    
    return run_simulation(G,seed)
    
    
def elegantify_layout(G, seed):
    '''
    Given networkx graph G and a layout, attempt to find an improvement
    to the layout and return it.
    '''
    return run_simulation(G,seed)
    
    
def demo():
    '''
    Run a demo showing how a random, ugly network graph evolves into
    a much nicer-looking graph.
    '''
    size = 8
    G = nx.gnm_random_graph(size,11)
    seed = nx.spring_layout(G)
    evol = run_simulation(G,seed)
    
    
def demo_evolution():
    '''
    Run a demo showing how a random, ugly network graph evolves into
    a much nicer-looking graph, using an asexually-reproducing
    evolutionary algorithm.
    '''
    size = 8
    G = nx.gnm_random_graph(size,11)
    seed = nx.spring_layout(G)
    evol = evolve_asexually(G,seed)
    
    
if __name__ == '__main__':
    demo()
