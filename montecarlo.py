#!usr/bin/python

import networkx as nx
import matplotlib.pyplot as plt
import random
from graph_geometry import *

# Montecarlo algorithm to supplant the asexually reproducing
# genetic algorithm.  It should be much simpler, since it won't have
# all the machinery of genetic algorithms.

# Uses tuple comparison:  It is true that (1,3) < (2,2)


def run_simulation(G, seed, k=500):
    
    layout, fitness = montecarlo(G, seed, count_crosses, no_crosses, mutation_rate=0.25, n=k)  # First minimise edge crossings
    layout, fitness = montecarlo(G, layout, calc_fitness, dummy, mutation_rate=0.2, n=k)  # Then prettify
    
    print 'Final fitness', fitness
    nx.draw(G, layout)
    plt.show()
    
    return layout
    
    
def montecarlo(G, seed, fitness_function, break_function, mutation_rate=0.1, n=10):
    
    layout = seed.copy()
    fitness = fitness_function(G, layout)
    best_fitness = fitness
    
    print 'Initial fitness', best_fitness
    nx.draw(G, layout)
    plt.show()
    
    for k in range(n):
            
        if break_function(fitness):
            break

        new_layout = layout.copy()
        
        for node in G.nodes():
            if random.random() < mutation_rate:
                #print 'mutating'
                new_layout[node] = random.random(), random.random()
                
        fitness = fitness_function(G, new_layout)
        #print 'Iterated, fitness is now:', fitness
        
        if fitness < best_fitness: # Improvement in fitness
            layout = new_layout
            best_fitness = fitness
            print k, 'gen, fitness is', best_fitness
            nx.draw(G, layout)
            plt.show()
    
    print 'Montecarlo done, fitness is:', fitness_function(G, layout)
    print
    
    return layout, best_fitness
        
        
def calc_fitness(G, layout):
    v1 = count_crosses(G, layout)
    v2 = total_node_on_edge_penalty(G, layout, 0.2)
    v3 = total_cosine_factors(G, layout)
    v4 = calc_length_std_dev(G, layout)
    return v1, v2, v3, v4


def no_crosses(fitness):
    if fitness == 0:
        return True
    else:
        return False

def dummy(fitness):
    return False

if __name__ == '__main__':
    size = 8
    G = nx.gnm_random_graph(size,11)
    seed = nx.spring_layout(G)
    
    layout = run_simulation(G, seed)

    print (1,3) < (2,2)
