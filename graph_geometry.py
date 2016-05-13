#!usr/bin/python

# Ideas for an algorithm to minimize edge crossings in a graph (network)

# This module contains functions that calculate geometric properties
# of graphs with a given layout.  Eg. number of edge crossings in the
# layout; and a penalty factor for how close a node is to an edge.

import networkx as nx
import math
from matplotlib import pyplot as plt


def crossproduct(P,Q):
    """Cross product of vectors in R2, expressed as 2-tuples, or lists."""
    return (P[0]*Q[1]) - (P[1]*Q[0])

def dotproduct(P,Q):
    return P[0]*Q[0] + P[1]*Q[1]

def detect_cross(A,B,C,D):
    """Given Cartesian coordinates of 4 points A, B, C, D,
       return True if lines AB and CD cross."""

    Ax, Ay = A[0], A[1]
    Bx, By = B[0], B[1]
    Cx, Cy = C[0], C[1]
    Dx, Dy = D[0], D[1]

    #  We assume A,B,C,D are all different nodes.
    #  i.e. have NOT been sent edges (A,B) and (A,C)
    #  So we can check for coincidence.

    if Ax == Bx and Ay == By: print "Coincidence"; return True
    if Ax == Cx and Ay == Cy: print "Coincidence"; return True
    if Ax == Dx and Ay == Dy: print "Coincidence"; return True
    if Bx == Cx and By == Cy: print "Coincidence"; return True
    if Bx == Dx and By == Dy: print "Coincidence"; return True
    if Cx == Dx and Cy == Dy: print "Coincidence"; return True

    AB = (Bx - Ax, By - Ay)
    AC = (Cx - Ax, Cy - Ay)
    AD = (Dx - Ax, Dy - Ay)

    CA = (Ax - Cx, Ay - Cy)
    CB = (Bx - Cx, By - Cy)
    CD = (Dx - Cx, Dy - Cy)

    BD = (Dx - Bx, Dy - By)
    DB = (Bx - Dx, By - Dy)

    # Generic cases where no three points are colinear.

    if crossproduct(AC,AD) > 0:
        if crossproduct(AC,AB) > 0:
            if crossproduct(AB,AD) > 0:
                # AB is heading towards crossing CD.
                if crossproduct(CB,CA) > 0:
                    if crossproduct(CB,CD) > 0:
                        if crossproduct(CD,CA) > 0:
#                           print "1 Edges cross! Dude!"
                            return True
                elif crossproduct(CB,CA) < 0:
                    if crossproduct(CB,CD) < 0:
                        if crossproduct(CD,CA) < 0:
#                           print "2 Edges cross! Dude!"
                            return True

    if crossproduct(AC,AD) < 0:
        if crossproduct(AC,AB) < 0:
            if crossproduct(AB,AD) < 0:
                # AB is heading towards crossing CD.
                if crossproduct(CB,CA) > 0:
                    if crossproduct(CB,CD) > 0:
                        if crossproduct(CD,CA) > 0:
#                           print "3 Edges cross! Dude!"
                            return True
                elif crossproduct(CB,CA) < 0:
                    if crossproduct(CB,CD) < 0:
                        if crossproduct(CD,CA) < 0:
#                           print "4 Edges cross! Dude!"
                            return True

    # Corner cases where a point is colinear with two others.
    # Cross detected if a point is ON the line segment.

    if crossproduct(AB,AC) == 0:
#       print "C is colinear with A and B."
        if dotproduct(AB,AC) > 0 and dotproduct(AC,CB) > 0:
            print "C is on line AB."
            return True

    if crossproduct(AB,AD) == 0:
#       print "D is colinear with A and B"
        if dotproduct(AB,AD) > 0 and dotproduct(AD,DB) > 0:
            print "D is on line AB."
            return True

    if crossproduct(CD,CA) == 0:
#       print "A is colinear with C and D."
        if dotproduct(CD,CA) > 0 and dotproduct(CA,AD) > 0:
            print "A is on line CD."
            return True

    if crossproduct(CD,CB) == 0:
#       print "B is colinear with C and D"
        if dotproduct(CD,CB) > 0 and dotproduct(CB,BD) > 0:
            print "B is on line CD."
            return True


    return False


def nx_detect_crosses(G, pos):
    return find_crossing_edges(G, pos)

def find_crossing_edges(G, pos):
    """Given graph G and positions 'pos',
       return list of edge pairs that cross."""
    crossing_edges = []
    for i, edge1 in enumerate(G.edges()):
        for edge2 in G.edges()[i+1:]:
            if edge1[0] in edge2 or edge1[1] in edge2:
                pass
            else:
                A = (pos[edge1[0]])
                B = (pos[edge1[1]])
                C = (pos[edge2[0]])
                D = (pos[edge2[1]])
    
                if detect_cross(A,B,C,D):
                    cross = (edge1,edge2)
                    crossing_edges.append(cross)

    return crossing_edges

def count_crosses(G,pos):
    """Given graph G and positions 'pos',
       return number of edge crossings."""
    num_crossings = 0

#   print "Edges of G:\n", G.edges()
    for i, edge1 in enumerate(G.edges()):
        for edge2 in G.edges()[i+1:]:
#           print "Consider cross of {} and {}".format(edge1,edge2)

            if edge1[0] in edge2 or edge1[1] in edge2:
                # Edges have a mutual node; cannot cross
                pass

            else:
#               print "Worth checking for cross."
                A = (pos[edge1[0]])
                B = (pos[edge1[1]])
                C = (pos[edge2[0]])
                D = (pos[edge2[1]])

                if detect_cross(A,B,C,D):
#                   print "                        cross detected!!!!"
                    num_crossings += 1

    return num_crossings


########################################################################
######################  Other Fitness Criteria

def node_to_cartesian(node,layout):
    """Returns cartesian coordinates of graph node."""
    A = layout[node]
    Ax, Ay = A[0], A[1]

    return Ax, Ay

def node_pair_to_cartesian(node1,node2,layout):
    """Given node1 and node2, returns cartesian coordinates
       of the two nodes as 4-tuple (node1_x,node1_y,node2_x,node2_y)"""

    Ax, Ay = node_to_cartesian(node1,layout)
    Bx, By = node_to_cartesian(node2,layout)

    return Ax, Ay, Bx, By

def edge_to_cartesian(edge, layout):
    """Given graph edge (node1,node2), returns cartesian coordinates
       of the two nodes as 4-tuple (node1_x,node1_y,node2_x,node2_y)"""

    node1 = edge[0]
    node2 = edge[1]

    Ax, Ay, Bx, By = node_pair_to_cartesian(node1,node2,layout)

    return Ax, Ay, Bx, By

def edge_to_vector(edge,layout):

    Ax, Ay, Bx, By = edge_to_cartesian(edge,layout)

    vector = (Bx - Ax, By - Ay)

    return vector

def dot_product(edge1,edge2,layout):
    vector1 = edge_to_vector(edge1,layout)
    vector2 = edge_to_vector(edge2,layout)

    dot_prod = dotproduct(vector1,vector2)

    return dot_prod

def calc_edge_length(edge, layout):
    """Given a graph edge, calculate its length in given layout."""

    Ax, Ay, Bx, By = edge_to_cartesian(edge,layout)

    edge_length = math.sqrt( (Bx - Ax)*(Bx - Ax) + (By - Ay)*(By - Ay) )

    #print edge, Ax, Ay, Bx, By

    return edge_length

def vector_length(vector):
    a, b = vector
    length = math.sqrt(a*a + b*b)
    return length

def edge_cosine(edge1,edge2,layout):
    vector1 = edge_to_vector(edge1,layout)
    vector2 = edge_to_vector(edge2,layout)

    dot_prod = dotproduct(vector1,vector2)

    length1 = vector_length(vector1)
    length2 = vector_length(vector2)

    cosine = dot_prod / (length1 * length2)
    if cosine > 1:
        print "Cosine cockup! ",cosine
        print "dot,l1,l2:",dot_prod,length1,length2
        cosine = 1
    elif cosine < -1:
        print "Cosine cockup! ",cosine
        print "dot,l1,l2:",dot_prod,length1,length2
        cosine = -1

    return cosine

def edge_angle(edge1,edge2,layout):
    cosine = edge_cosine(edge1,edge2,layout)

    angle = math.acos(cosine)

    return angle



def calc_internode_distance(node1,node2,layout):
    Ax, Ay, Bx, By = node_pair_to_cartesian(node1,node2,layout)

    internode_distance = math.sqrt( (Bx - Ax)*(Bx - Ax) + (By - Ay)*(By - Ay) )

    return internode_distance

def calc_mean_edge_length(G,layout):
    lengths = [ calc_edge_length(edge,layout) for edge in G.edges() ]
    n = len(lengths)

    mean = sum(lengths) / n

    return mean

def calc_mean_min_length_ratio(G,layout):

    lengths = [ calc_edge_length(edge,layout) for edge in G.edges() ]
    n = len(lengths)
    min_length = min(lengths)
    mean_length = sum(lengths) / n

    mean_min_ratio = float(mean_length)/(min_length)

    #print total_length, min_length

    return mean_min_ratio

def calc_length_std_dev(G,layout):

    lengths = [ calc_edge_length(edge,layout) for edge in G.edges() ]
    n = len(lengths)

    mean = sum(lengths) / n
    #print "mean: ", mean

    anomalies = [ length - mean for length in lengths ]
    variances = [x*x for x in anomalies ]
    variance = sum(variances) / n
    std_dev = math.sqrt(variance)

    return std_dev

def node_in_edge_ellipse(node,edge,gap,layout):
    edge_length = calc_edge_length(edge,layout)
    rope_length = edge_length + gap

    distance1 = calc_internode_distance(edge[0],node,layout)
    distance2 = calc_internode_distance(edge[1],node,layout)

    if distance1 + distance2 < rope_length:
        return True
    else:
        return False

def count_nodes_in_edge_ellipses(G,layout,gap_factor):

    gap = gap_factor * calc_mean_edge_length(G,layout)

    count = 0

    for edge in G.edges():
        for node in G.nodes():
            if node in edge:
                pass
            else:
                if node_in_edge_ellipse(node,edge,gap,layout):
                    count += 1
    return count

def ellipse_intrusion_distance(node,edge,gap,layout):
    edge_length = calc_edge_length(edge,layout)
    rope_length = edge_length + gap + gap

    distance1 = calc_internode_distance(edge[0],node,layout)
    distance2 = calc_internode_distance(edge[1],node,layout)

    intrusion_distance = rope_length - (distance1 + distance2)

    if intrusion_distance > 0:
        print "For edge ellipse",edge,"node",node,"intrudes",intrusion_distance
        return intrusion_distance
    else:
        return 0

def total_ellipse_intrusion(G,layout,gap_factor):
    mean = calc_mean_edge_length(G,layout)
    gap = gap_factor * mean

    intrusion = 0.0

    for edge in G.edges():
        for node in G.nodes():
            if node in edge:
                pass
            else:
                intrusion += ellipse_intrusion_distance(node,edge,gap,layout)

    return intrusion/mean

def node_on_edge_penalty(node,edge,gap,layout):
    edge_length = calc_edge_length(edge,layout)
    rope_length = edge_length + gap + gap

    distance1 = calc_internode_distance(edge[0],node,layout)
    distance2 = calc_internode_distance(edge[1],node,layout)

    intrusion_distance = rope_length - (distance1 + distance2)

    if intrusion_distance > 0:
        penalty_length = distance1 + distance2 - edge_length
        if penalty_length < 0:  # Physically impossible, but happens due to numerics.
            penalty_factor = 999
        else:
            penalty_fac = edge_length/penalty_length
            penalty_factor = min( int(penalty_fac), 999)
        #print "Ellipse",edge,"node",node,"intrudes",intrusion_distance,"penalty",penalty_factor
        return penalty_factor
    else:
        return 0

def total_node_on_edge_penalty(G,layout,gap_factor=0.2):
    mean = calc_mean_edge_length(G,layout)
    gap = gap_factor * mean

    penalty = 0.0

    for edge in G.edges():
        for node in G.nodes():
            if node in edge:
                pass
            else:
                penalty += node_on_edge_penalty(node,edge,gap,layout)

    return penalty


######################################################################
######################   Edge Angle Stuff

def edges_of_node(node,G,layout):
    edges = []
    for edge in G.edges():
        if node in edge:
            if edge[0] == node:
                edges.append(edge)
            else:
                flipped_edge = (edge[1],edge[0])
                edges.append(flipped_edge)
    return edges

def edge_dot_products(node_edges, layout):
    dot_product_list = []
    for i, edge1 in enumerate(node_edges):
        for edge2 in node_edges[i+1:]:
            vector1 = edge_to_vector(edge1,layout)
            vector2 = edge_to_vector(edge2,layout)
            dot_prod = dot_product(edge1,edge2,layout)
            dot_product_list.append(dot_prod)
            #print "dot of " + str(edge1) + str(edge2) + " is "
            #print str(vector1) +str(vector2) + " : " + str(dot_prod)

    return dot_product_list

def total_node_dot_products(G,layout):
    total = 0
    for node in G:
        node_edges = edges_of_node(node,G,layout)
        node_dot_products = edge_dot_products(node_edges,layout)
        subtotal = sum(node_dot_products)
        total += subtotal

    return total


def edge_angles(node_edges, layout):
    angle_list = []
    for i, edge1 in enumerate(node_edges):
        for edge2 in node_edges[i+1:]:
            angle = edge_angle(edge1,edge2,layout)
            angle_list.append(angle)

    return angle_list

def total_edge_angles(G,layout):
    total = 0
    for node in G:
        node_edges = edges_of_node(node,G,layout)
        node_edge_angles = edge_angles(node_edges,layout)
        subtotal = sum(node_edge_angles)
        total += subtotal

    return total


def total_angle_exp(G,layout):
    total = 0
    for node in G:
        node_edges = edges_of_node(node,G,layout)
        node_edge_angles = edge_angles(node_edges,layout)

        factors = [math.exp(-x) for x in node_edge_angles]

        subtotal = sum(factors)
        total += subtotal

    return total

def avg_angle_exp(G,layout):
    total = 0
    num_adj_angles = 0

    for node in G:
        node_edges = edges_of_node(node,G,layout)
        node_edge_angles = edge_angles(node_edges,layout)

        factors = [math.exp(-x) for x in node_edge_angles]

        subtotal = sum(factors)
        total += subtotal
        num_adj_angles += len(factors)

    avg = total/num_adj_angles

    #print "total:",total,"avg",avg
    return avg


def total_node_cosines(node_edges, layout):
    total = 0
    
    for i, edge1 in enumerate(node_edges):
        for edge2 in node_edges[i+1:]:
            cosine = edge_cosine(edge1,edge2,layout)
            total += cosine
    
    return total


def total_cosines(G, layout):
    total = 0
    
    for node in G:
        node_edges = edges_of_node(node, G, layout)
        node_cosines =  total_node_cosines(node_edges, layout)
        total += node_cosines
        
    return total
    
    
def total_node_cosine_factors(node_edges, layout):
    total = 0.0
    
    for i, edge1 in enumerate(node_edges):
        for edge2 in node_edges[i+1:]:
            cosine = edge_cosine(edge1,edge2,layout)
            cosine_factor = 1.0/(1.1 - cosine) - 0.476190
            total += cosine_factor
    
    return total


def total_cosine_factors(G, layout):
    total = 0.0
    
    for node in G:
        node_edges = edges_of_node(node, G, layout)
        node_cosine_factors =  total_node_cosine_factors(node_edges, layout)
        total += node_cosine_factors
        
    return total


