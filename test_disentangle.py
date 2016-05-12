#!usr/bin/python

import unittest
import networkx as nx
import matplotlib.pyplot as plt
from montecarlo import run_simulation

class TestDisentangle(unittest.TestCase):
    
    def test_triangle(self):
        G = nx.Graph()
        G.add_edges_from([(1,2), (1,3), (2,3)])
        layout = {1: (0.2,0.2), 2: (0.8, 0.2), 3: (0.5, 0.8)}
        
        run_simulation(G, layout)
    
    def test_widening(self):
        G = nx.Graph()
        G.add_edges_from([(1,3), (2,3)])
        layout = {1: (0.2,0.2), 2: (0.8, 0.2), 3: (0.5, 0.8)}
        
        run_simulation(G, layout)
    
    def test_rhombus(self):
        G = nx.Graph()
        G.add_edges_from([(1,2), (2,3), (3,4), (4,1)])
        layout = {1: (0.2,0.2), 2: (0.5, 0.2), 3: (0.8, 0.8), 4: (0.5,0.8)}
        
        run_simulation(G, layout)
        
if __name__ == '__main__':
    unittest.main()
