#!usr/bin/python

# Ideas for an algorithm to minimize edge crossings in a graph (network)

import networkx as nx
import math
from matplotlib import pyplot as plt

class Node(object):
	def __init__(self, x_coord,y_coord):
		self.x = x_coord
		self.y = y_coord
	
class Edge(object):
	def __init__(self, start_node, end_node):
		self.node1 = start_node
		self.node2 = end_node
	
# Given x,y coordinates of two edges, need to detect if they cross

def crossproduct(A,B):
	"""Cross product of vectors in R2, expressed as 2-tuples, or lists."""
	Xp = (A[0]*B[1]) - (A[1]*B[0])
	return Xp

def detect_cross(edge1, edge2):
	"""Given two edges, detect if they cross."""
	
	Ax = float(edge1.node1.x)
	Ay = float(edge1.node1.y)
	Bx = float(edge1.node2.x)
	By = float(edge1.node2.y)

	Cx = float(edge2.node1.x)
	Cy = float(edge2.node1.y)
	Dx = float(edge2.node2.x)
	Dy = float(edge2.node2.y)

	AB = (Bx - Ax, By - Ay)
	AC = (Cx - Ax, Cy - Ay)
	AD = (Dx - Ax, Dy - Ay)
	
	CA = (Ax - Cx, Ay - Cy)
	CB = (Bx - Cx, By - Cy)
	CD = (Dx - Cx, Dy - Cy)

	if crossproduct(AC,AD) > 0:
		if crossproduct(AC,AB) > 0:
			if crossproduct(AB,AD) > 0:
				# AB is heading towards crossing CD.
				if crossproduct(CB,CA) > 0:
					if crossproduct(CB,CD) > 0:
						if crossproduct(CD,CA) > 0:
#							print "Edges cross! Dude!"
							return 1
				elif crossproduct(CB,CA) < 0:
					if crossproduct(CB,CD) < 0:
						if crossproduct(CD,CA) < 0:
#							print "Edges cross! Dude!"
							return 1
	
	elif crossproduct(AC,AD) < 0:
		if crossproduct(AC,AB) < 0:
			if crossproduct(AB,AD) < 0:
				# AB is heading towards crossing CD.
				if crossproduct(CB,CA) > 0:
					if crossproduct(CB,CD) > 0:
						if crossproduct(CD,CA) > 0:
#							print "Edges cross! Dude!"
							return 1
				elif crossproduct(CB,CA) < 0:
					if crossproduct(CB,CD) < 0:
						if crossproduct(CD,CA) < 0:
#							print "Edges cross! Dude!"
							return 1

	else: return 0


A = Node(0,0)
B = Node(10,10)
C = Node(2,1)
D = Node(7,9)

print "A.x: ", A.x

edsel = Edge(A,B)
edgar = Edge(C,D)

print "Do edsel and edgar cross?", detect_cross(edsel,edgar)

print "\nNow to create a bunch of objects..."

positions = [(0,0),(2,0),(4,0),(0,1),(2,1),(4,1)]
nodes = [Node(x,y) for x,y in positions]

print "node list indexing.  nodes[2].x is", nodes[2].x

edgeindices = [(0,1),(0,3),(0,4),(1,3),(1,4),(1,5),(2,5)]

edges = [Edge(nodes[i], nodes[j]) for i,j in edgeindices]

print "Detect cross of edge2 and edge3...", detect_cross(edges[2], edges[3])

print "\n\n" + "#" * 50
print "Using networkx...\n"


#######################################################################
##########  Do it using networkx


def nx_detect_crosses(G, pos):
	"""Given graph G and positions 'pos',
	   return list of edge pairs that cross."""
	crossing_edges = []
	for i, edge1 in enumerate(G.edges()):
		for edge2 in G.edges()[i:]:
			A = (pos[edge1[0]])
			B = (pos[edge1[1]])
			C = (pos[edge2[0]])
			D = (pos[edge2[1]])
			
			if _detect_cross(A,B,C,D):
				cross = (edge1,edge2)
				crossing_edges.append(cross)
				
	return crossing_edges
	
def _detect_cross(A,B,C,D):
	"""Given Cartesian coordinates of 4 points A, B, C, D,
	   return True if lines AB and CD cross."""


	Ax, Ay = A[0], A[1]
	Bx, By = B[0], B[1]
	Cx, Cy = C[0], C[1]
	Dx, Dy = D[0], D[1]

	AB = (Bx - Ax, By - Ay)
	AC = (Cx - Ax, Cy - Ay)
	AD = (Dx - Ax, Dy - Ay)
	
	CA = (Ax - Cx, Ay - Cy)
	CB = (Bx - Cx, By - Cy)
	CD = (Dx - Cx, Dy - Cy)

	if crossproduct(AC,AD) > 0:
		if crossproduct(AC,AB) > 0:
			if crossproduct(AB,AD) > 0:
				# AB is heading towards crossing CD.
				if crossproduct(CB,CA) > 0:
					if crossproduct(CB,CD) > 0:
						if crossproduct(CD,CA) > 0:
#							print "Edges cross! Dude!"
							return True
				elif crossproduct(CB,CA) < 0:
					if crossproduct(CB,CD) < 0:
						if crossproduct(CD,CA) < 0:
#							print "Edges cross! Dude!"
							return True
	
	elif crossproduct(AC,AD) < 0:
		if crossproduct(AC,AB) < 0:
			if crossproduct(AB,AD) < 0:
				# AB is heading towards crossing CD.
				if crossproduct(CB,CA) > 0:
					if crossproduct(CB,CD) > 0:
						if crossproduct(CD,CA) > 0:
#							print "Edges cross! Dude!"
							return True
				elif crossproduct(CB,CA) < 0:
					if crossproduct(CB,CD) < 0:
						if crossproduct(CD,CA) < 0:
#							print "Edges cross! Dude!"
							return True

	else: return False

def crossproduct(P,Q):
	"""Cross product of vectors in R2, expressed as 2-tuples, or lists."""
	Xp = (P[0]*Q[1]) - (P[1]*Q[0])
	return Xp

def all_pair_swaps(G,start_pos):
	"""Given a starting layout, swap positions of all possible
	   node pairs, to minimize edge crossings."""
	
	start_crossings = len(nx_detect_crosses(G,start_pos))
	best_crossings = start_crossings
	best_pos = start_pos.copy()

	for i, node1 in enumerate(G.nodes()):
		for node2 in G.nodes()[i+1:]:
			pos = start_pos.copy()
			dummy = pos[node1]
			pos[node1] = pos[node2]
			pos[node2] = dummy
			crossings = len(nx_detect_crosses(G,pos))
			#print "Swap {} and {}".format(node1,node2)
			
			if crossings < start_crossings:
				#print "Swapping {} and {} reduces crossings to {}".format(node1,node2,crossings)
				if crossings < best_crossings:
					best_crossings = crossings
					print "Swapping {} and {} reduces crossings to {}".format(node1,node2,crossings)
					#print "best crossings ",best_crossings
					best_pos = pos.copy()
				
	return best_pos


def circular_iter(G, start_pos=None):
	if start_pos == None: start_pos = nx.circular_layout(G)
	
	best_pos = start_pos.copy()
	
	best_crossings = len(nx_detect_crosses(G,best_pos))
	if best_crossings == 0:
		return best_pos
	
	for x in range(1,len(G.nodes())):
		print "\nIteration number:",x
		
		new_pos = all_pair_swaps(G, best_pos)
		new_crossings = len(nx_detect_crosses(G,new_pos))
		
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
		


########################################################################

#~ nodes = [0,1,2,3,4,5]
#~ positions = [(0,0),(2,0),(4,0),(0,1),(2,1),(4,1)]
#~ edges = [(0,1),(0,3),(0,4),(1,3),(1,4),(1,5),(2,5)]
#~ 
#~ G = nx.Graph()
#~ G.add_edges_from(edges)
#~ print "G nodes ",G.nodes()
#~ print "G edges ", G.edges()
#pos = {node:xy for node, xy in zip(G.nodes(),positions)}
#print "pos dictionary ", pos

#~ crossings = nx_detect_crosses(G, pos)
#~ print "There are {} edge crossings: {}".format(len(crossings),crossings)
#~ nx.draw(G,pos)
#~ plt.show()

print "Generating random graph...\n"

G =nx.gnm_random_graph(10,12)

pos1 = nx.spring_layout(G)
crossings = nx_detect_crosses(G, pos1)
print "\nFor nx spring layout..."
print "There are {} edge crossings: {}".format(len(crossings),crossings)
nx.draw(G,pos1)
plt.show()


pos2 = nx.circular_layout(G)
crossings = nx_detect_crosses(G, pos2)
print "\nFor nx circular layout..."
print "There are {} edge crossings: {}".format(len(crossings),crossings)
nx.draw(G,pos2)
plt.show()

pos3 = circular_iter(G,pos2)
crossings = nx_detect_crosses(G, pos3)
print "\ncircle swapped, There are {} edge crossings: {}".format(len(crossings),crossings)
nx.draw(G,pos3)
plt.show()

pos4 = nx.spring_layout(G,2, pos3)
crossings = nx_detect_crosses(G, pos4)
print "\nFor nx spring layout AFTER circle swap ..."
print "There are {} edge crossings: {}".format(len(crossings),crossings)
nx.draw(G,pos4) 
plt.show()


#  Okay, edge cross detection working well with networkx.
#  Now to move nodes around to minimize edge crossings.

