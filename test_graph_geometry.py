#!usr/bin/python

# Ideas for an algorithm to minimize edge crossings in a graph (network)

# This module runs the test suite for graph geometry functions.

import unittest
from graph_geometry import *
from layout_generators import *

class TestGraphGeometry(unittest.TestCase):
        
    def test_detect_cross(self):
    
        A = [0,0]
        B = [2,0]
    
        C, D = [0,-1], [1,1]
        print "Simple cross. Detect cross?", detect_cross(A,B,C,D)
    
        C, D = (1,1), (2,-1)
        print "Second Simple cross. Detect cross?", detect_cross(A,B,C,D)
    
        C, D = (0,0), (1,1)
        print "Coincident points A and C.  Detect cross?", detect_cross(A,B,C,D)
        print "Must assume A,B,C,D are distinct nodes. i.e. NOT like edges (0,1) and (0,2)"
    
        C, D = (1,0), (1,1)
        print "Point C on line AB.  Detect cross?", detect_cross(A,B,C,D)
    
        C, D = (1,0), (3,0)
        print "Lines AB and CD overlap.  Detect cross?", detect_cross(A,B,C,D)
    
        C, D = (3,0), (5,0)
        print "Lines AB and CD lie on same line but don't touch.  Detect cross? (shouldn't)", detect_cross(A,B,C,D)
    
        C, D = (0,-1), (0,1)
        print "Point A on vertical line CD.  Detect cross?", detect_cross(A,B,C,D)
    
        print
    
        print "All good, now test with nx generated layout.\n"
    
        G =nx.gnm_random_graph(10,15)
    
        rand = nx.random_layout(G)
        print "random layout:"
        print rand
    
        print "\nNumber of crosses:", count_crosses(G,rand)
        
    
    def test_nx_detect_crosses(self):
        nodes = [0,1,2,3,4,5]
        positions = [(0,0),(2,0),(4,0),(0,1),(2,1),(4,1)]
        edges = [(0,1),(0,3),(0,4),(1,3),(1,4),(1,5),(2,5)]
    
        G = nx.Graph()
        G.add_edges_from(edges)
        print "G nodes ",G.nodes()
        print "G edges ", G.edges()
        pos = {node:xy for node, xy in zip(G.nodes(),positions)}
        print "pos dictionary ", pos
    
        crossings = nx_detect_crosses(G, pos)
        print "There are {} edge crossings: {}".format(len(crossings),crossings)
        nx.draw(G,pos)
        plt.show()

    
    def test_ellipse_stuff(self):
        G = nx.gnm_random_graph(10,15)
        pos = nx.random_layout(G)
    
        intrusion = total_ellipse_intrusion(G,pos,0.2)
        print "Intrusion:", intrusion
    
        nx.draw(G,pos)
        plt.show()
    
    def test_node_on_edge_stuff(self):
        G = nx.gnm_random_graph(10,15)
        pos = nx.random_layout(G)
    
        penalty = total_node_on_edge_penalty(G,pos,0.2)
        print "Total node on edge penalty:", penalty
    
        nx.draw(G,pos)
        plt.show()
    
    
    def test_edge_length_stuff(self):
        G = nx.gnm_random_graph(10,15)
        pos = tripod_layout(G)
    
        print pos
        print G.edges()
    
        for edge in G.edges():
            print calc_edge_length(edge,pos)
    
        print "Mean edge length as multiple of shortest edge length: ", calc_mean_min_length_ratio(G,pos)
        print "Edge length std dev: ", calc_length_std_dev(G,pos)


    def test_edges_of_node(self):
        G = nx.gnm_random_graph(4,6)
        layout = nx.random_layout(G)
    
        for node in G:
            print node
            node_edges = edges_of_node(node,G,layout)
            print node_edges
            print edge_dot_products(node_edges,layout)
        print
    
        nx.draw(G,layout)
        plt.show()
    
    def test_total_dotty(self):
        G = nx.gnm_random_graph(4,6)
        layout = nx.random_layout(G)
    
        print total_node_dot_products(G,layout)
    
        nx.draw(G,layout)
        plt.show()


if __name__ == '__main__':
    unittest.main()
