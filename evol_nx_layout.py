#!usr/bin/python

import networkx as nx
import matplotlib.pyplot as plt
import random
from graph_geometry import *
import disentangler as dis

# Ideas for an algorithm to minimize edge crossings in a graph (network)

# Genetic algorithms to find a layout that minimises edge crossings.

#############  Sexual Reproduction with Mutation

def procreate(parent1,parent2,mutation_rate=0.1):
    """Given two parents, generate a child, each of whose genes
       has a probability `mutation_rate' of being a random
       mutation, and if not a mutation, a 50% probability of
       deriving from each parent."""

    mutants = nx.random_layout(G)

    child = {}

    for k in range(size):
        if random.random() < mutation_rate:
            child[k] = mutants[k]
        else:
            if random.random() < 0.5:
                child[k] = parent1[k]
            else:
                child[k] = parent2[k]

    return child

def fructify(seed1,seed2,n=4):
    """Given two parents, generate n children."""

    pool = [(count_crosses(G,seed1),seed1),
            (count_crosses(G,seed2),seed2)]

    for k in range(n):
        child = procreate(seed1,seed2)
        pool.append(( count_crosses(G,child),child) )

    #pool.sort()
    return pool


def select_best_pair(pool):
    """Given a pool - two parents and all children -
       select the fittest."""

    hacklist = []
    for k, item in enumerate(pool):
        fitness = str(item[0])
        index = str(k)
        hack = float(fitness + "." + index)
        hacklist.append(hack)

    hacklist.sort()

    print "Hacklist:  ", hacklist

    winner1code = str(hacklist[0])
    winner2code = str(hacklist[1])

    winner1index = int(winner1code.split(".")[1])
    winner2index = int(winner2code.split(".")[1])

    winner1 = pool[winner1index][1]
    winner2 = pool[winner2index][1]

    return winner1, winner2

def rank(pool):
    """Given pool, sort into order of descending fitness.
        Dunno how to do this yet..."""

    #scores = [count_crosses(pos) for pos in pool]

def evolve(seed1,seed2,gens=10):
    """Given two seed ancestors, inbreed for gens generations,
       with only the fittest pair breeding."""

    winner1 = seed1
    winner2 = seed2

    for k in range(gens):
        pool = fructify(winner1,winner2)
        winner1, winner2 = select_best_pair(pool)

        #~ if winner1.all() == winner2.all():  # Need to get this going.
            #~ print "Clones!"
            #~ break

        #~ nx.draw(G,pos=winner1)
        #~ plt.title("Iteration ")
        #~ plt.show()
        #~ nx.draw(G,pos=winner2)
        #~ plt.show()
    #~
    return winner1

###########################   Asexual Reproduction with Mutation

def multiply(G,seed,num_offspring=10, mutation_rate=0.5,SpringOffspring = True):
    size = len(G)  # Number of nodes in graph G.

    if mutation_rate < 1.0/size:  # So at least one node (on average) is mutated.
        mutation_rate = 1.0/size

    pool = [seed]
    pool_size = 1

    if SpringOffspring:  # First offspring is good ol' spring layout.
        pool.append(nx.spring_layout(G,pos=seed))
        pool_size = 2

    for k in range(3 * num_offspring):  # Prevents infinite loop.
        mutants = nx.random_layout(G)
        child = {}

        NotaClone = False

        for k in range(size):
            if random.random() < mutation_rate:
                child[k] = mutants[k]
                NotaClone = True
            else:
                child[k] = seed[k]

        if NotaClone:
            pool.append(child)
            pool_size += 1
        #else:
            #print "Clone! #####################################"

        if pool_size == num_offspring + 2:
            break

    return pool

def eval_fitness(G,layout):
    """Evaluate the fitness of a layout,
       where fitness is a single number to be minimised.
       At present, fitness = cross_count + node_on_edge_penalty,
       where node_on_edge_penalty is inversely proportional to
       distance of an node from an edge it is too close to."""
    cross_count = count_crosses(G,layout)
    #std_dev = calc_length_std_dev(G, layout)
    #fitness = cross_count + std_dev
    #print "cross count: ",cross_count, "std dev: ", std_dev, "fitness: ", fitness

    #length_ratio = calc_mean_min_length_ratio(G,layout)
    #fitness = cross_count + (length_ratio - 1)/10
    #print "cross count:", cross_count, " ratio:", length_ratio, " fitness:", fitness

    gap_factor = 0.2

    #ellipse_count = count_nodes_in_edge_ellipses(G,layout,gap_factor)
    #fitness = cross_count + float(ellipse_count)/10 + float(std_dev)/10
    #print "crosses:", cross_count, " ellipse:", ellipse_count, "std dev:", std_dev, " fitness:", fitness

    #ellipse_intrusion = total_ellipse_intrusion(G,layout,gap_factor)
    #fitness = cross_count + ellipse_intrusion
    #print "cross count:", cross_count, " intrusion:", ellipse_intrusion, " fitness:", fitness

    node_edge_penalty = total_node_on_edge_penalty(G,layout,gap_factor)
    #std_dev = calc_length_std_dev(G, layout)
    #fitness = cross_count + node_edge_penalty/1000 + std_dev/1000
    #print "crosses:", cross_count, " penalty:", node_edge_penalty,"stddev:",std_dev, " fitness:", fitness
    # This works very well.  Only weakness is that it does not select for symmetry.
    # How to describe symmetry of a graph?

    # Minimizing total adjacent edge dot products may select for symmetry
    #adjacent_dotps = total_node_dot_products(G,layout)
    #fitness = cross_count + node_edge_penalty/1000 + adjacent_dotps/1000
    #print "crosses:", cross_count, " penalty:", node_edge_penalty,"adjdots:",adjacent_dotps, " fitness:", fitness

    # Minimizing exp(-theta) for all angles theta may work...
    angle_factor = total_angle_exp(G,layout)
    fitness = cross_count + node_edge_penalty/1000 + angle_factor/1000
    print "crosses:", cross_count, " penalty:", node_edge_penalty,"angle exp:",angle_factor, " fitness:", fitness



    return fitness

def select_most_fit(G,pool):
    """Select most fit member of pool,
       where fitness is a single number to be minimised."""
    best = pool[0]
    best_fitness = eval_fitness(G,best)

    for thing in pool:
        fitness = eval_fitness(G,thing)
        if fitness < best_fitness:
            best = thing
            best_fitness = fitness

    return best, best_fitness

def asexual_evolve(G,seed,gens=15):
    mutation_rate = 0.5

    for k in range(gens):
        pool = multiply(G,seed,10,mutation_rate)
        winner, fitness = select_most_fit(G,pool)
        print "fitness of pool winner: ",fitness

        seed = winner

        if fitness < 1: mutation_rate = 0.2

    print "After ",gens," gens, Winner's Fitness: ", fitness
    return winner, fitness

######################################################################
#############   New Improved Asexual Evolution with Mutation

def fitness_tuple(G,layout):
    """Returns tuple of all fitness metrics."""
    cross_count = count_crosses(G,layout)
    gap_factor = 0.2
    node_edge_penalty = total_node_on_edge_penalty(G,layout,gap_factor)
    angle_factor = avg_angle_exp(G,layout)
    std_dev = calc_length_std_dev(G, layout)

    return (cross_count,node_edge_penalty,angle_factor,std_dev)

def fitness_filter(G,pool):
    """Finds fittest of pool by sequentially filtering by fitness
     metrics, from most to least important metric.
     Bung.   Angle metric often drives worse std dev.
     Need to reverse this."""

     # Cross count is most important.
    cross_counts = [count_crosses(G,layout) for layout in pool]
    least_count = min(cross_counts)

    winners = [(k,count) for k,count in enumerate(cross_counts) if count <= least_count]

    # Getting nodes off edges is next most important.
    gap_factor = 0.2
    node_edge_factors = [ total_node_on_edge_penalty(G,pool[k],gap_factor) for k,count in winners]
    least_node_factor = min(node_edge_factors)

    #print "zip" ,zip(winners,node_edge_factors)
    node_winners = [(k,c,nf) for (k,c),nf in zip(winners,node_edge_factors) if nf <= least_node_factor]

    # Now maximise angles
    angle_factors = [avg_angle_exp(G,pool[k]) for k,count,node_factor in node_winners]
    least_angle_factor = min(angle_factors)

    ang_winners = [(k,c,nf,af) for (k,c,nf),af in zip(node_winners,angle_factors) if af <= least_angle_factor]

    # Finally minimize std deviation of edge lengths.
    std_devs = [calc_length_std_dev(G,pool[k]) for k,cnt,nf,af in ang_winners]
    least_sd = min(std_devs)

    sd_winners = [(k,cnt,nf,af,sd) for (k,cnt,nf,af),sd in zip(ang_winners,std_devs) if sd <= least_sd]

    if len(sd_winners) > 1:
        print "More than 1 winner!"
        print sd_winners

        #~ print "cross counts",cross_counts
        #~ print "winners",winners
        #~ print "node edge factors",node_edge_factors
        #~ print "node winners",node_winners
        #~ print "angle factors",angle_factors
        #~ print "std devs",std_devs
        #~ print "sd winners",sd_winners

    wint = sd_winners[0] # First tuple from list of winners
    winner = pool[wint[0]]
    fitness = (wint[1],wint[2],wint[3],wint[4])

    if True:
        #print "Spring fitness", fitness_tuple(G,pool[1])

        if wint[0] == 0:
            print "Seed won."
        elif wint[0] == 1: # Index of spring layout
            print "Spring layout won!"
        else:
            print "winning k",wint[0],"len pool",len(pool)

    return winner, fitness

def filter_by(indices,pool,function):
    """Take pool members indexed by 'indices'
    Apply 'function' to those members.  For the members with
    the lowest value of 'function',
     return tuples of their indices and function values. """

    metrics = [function(G,pool[k]) for k in indices]
    least_metric = min(metrics)

    winners = [(k,metric) for k,metric in zip(indices,metrics) if metric <= least_metric]

    return winners

def fitness_fiddler(winners,fitness_matrix):
    indices = []
    for index,metric in winners:
        fitness_matrix[index].append(metric)
        indices.append(index)

    return indices, fitness_matrix

def fitness_filterer(G,pool):
    """Refactored fitness_filter.
    Working.
    Problem: Minimzing avg_angle_exp will stretch a triangle if there
    is a 'leaf' on one node.
    Fixed: Now Cosine = dot(a,b)/(|a|*|b|)  note brackets.
    Previously Cosine = dot(a,b)/|a|*|b|
    Problem: Evolves quite slowly. """

    indices = range(len(pool))
    fitness_matrix = [ [] for x in indices]

    metric_functions = (count_crosses,total_node_on_edge_penalty,avg_angle_exp)

    for function in metric_functions:

        winners = filter_by(indices, pool, function)
        indices, fitness_matrix = fitness_fiddler(winners, fitness_matrix)

        #print "indices:",indices
        if len(winners) == 1:
            break

    winning_k = winners[0][0]
    winner = pool[winning_k]
    fitness = fitness_matrix[winning_k]

    #print "Winners: ", winners
    #print "winning k:", winning_k, "Winners fitness: ",fitness

    return winner, fitness

def evolve_asexually(G,seed,gens=100):
    """New version of asexual evolve. Stops to plot graph
    if and only if a fitter layout evolves."""

    best_fitness = fitness_tuple(G,seed)
    print "Fitness of seed:",best_fitness
    nx.draw(G,seed)
    plt.show()

    snapshot_fitness = best_fitness

    mutation_rate = 0.5
    for k in range(1,gens+1):
        pool = multiply(G,seed,10,mutation_rate)
        winner, fitness = fitness_filterer(G,pool)

        seed = winner
        best_fitness = fitness

        if fitness[0] == 0: mutation_rate = 0.2

        if k % 5 == 0:
            if snapshot_fitness != fitness:
                snapshot_fitness = fitness
                print "Fitness of gen ",k," winner:",fitness
                nx.draw(G,winner)
                plt.show()

    print
    print "Evolution finished after ",k," generations."
    print "Winner's fitness: ",fitness
    nx.draw(G,winner)
    plt.show()

    return winner


#############################################   Main Bit

size = 8
G = nx.gnm_random_graph(size,11)

if True:
    seed = nx.spring_layout(G)
    evol = evolve_asexually(G,seed)

    # Now get this working
    #new = nx.spring_layout(G,evol)
    #nx.draw(G,new)
    #plt.show()

if False:  # Asexual Evolution
    seed = nx.random_layout(G)
    #seed = nx.circular_layout(G)
    #seed = dis.tripod_layout(G)
    nx.draw(G, pos=seed)
    plt.show()

    for k in range(15):
        winner, fitness = asexual_evolve(G,seed)
        seed = winner


        nx.draw(G, pos=winner)
        plt.show()

        #if fitness < 1: break

##    Wow!  Asexual reproduction works extremely well!
##    But optimum results are often still ugly.
##    Need to implement fitness criteria involving
##    having most arc lengths of similar lengths,
##    or having most angles not too narrow.

if False:   # Sexual Reproduction
    seed1 = nx.random_layout(G)
    seed2 = nx.random_layout(G)
    #seed2 = dis.tripod_layout(G)

    nx.draw(G, pos=seed1)
    plt.show()
    nx.draw(G, pos=seed2)
    plt.show()


    for k in range(10):
        winner = evolve(seed1,seed2)

        nx.draw(G, pos=winner)
        plt.show()

# Works.  But can find optimum solution then get worse!
# This is due to pair breeding -- the inferior parent pollutes the genes.

## Works.  But gets stuck in local minimum.  No mutation yet.
## Winner take all breeding -- only best pair get to breed.


##########################################  Testing

#a = [(3,"d"),(3,"b"),(1,"c")]
#a.sort()
#print "\n a, eh.",a
#pool.sort()  # Fails...
# Appears to sort by second tuple element if first elements are same.
# Need to sort by first tuple value only.

#~ a = [3,2,1]
#~ b = ["a","b","c"]
#~
#~ c = zip(a,b)
#~
#~ print c
#~ c.sort()
#~
#~ print c

#print "\nRandom? ", random.random()
