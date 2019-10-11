import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from util import *
import pandas as pd
import scipy.stats as stats


G = nx.read_gml('power.gml', None)
degreeFrequencies = np.array(nx.degree_histogram(G))
degrees = [i[1] for i in G.degree]

# print(nx.info(G))
'''
Number of nodes: 4941
Number of edges: 6594
Average degree:   2.6691
'''
'''
density = nx.density(G)                             # 0.0005403026973346214
globalclusteringCoefficient = nx.transitivity(G)    # 0.10315322452860086
localClusteringCoefficients = nx.clustering(G)
aspl = nx.average_shortest_path_length(G)             # 18.989185424445708
'''

# Normal Scale
# plotDegreeDistribution(degreeFrequencies, logScale=False)

# Logarithmic scale
# plotDegreeDistribution(degreeFrequencies, logScale=True)

# With Power law plot
# computePowerLawFitValues(degrees)
# alpha(10.43584815827752) sigma(1.308516706237002)
# loglikelihoodRatio(-0.9185063058809141) pVal(0.16159229772218375)

# drawDegreeDistributionWithPowerLaw(degrees)

# drawGraphQuantile(G)

# remove one (or both) of the nodes with +15 links and draw graph
# Hubs: node 4458 - 18 links
#       node 2553 - 19 links

G.remove_node(4458)
G.remove_node(2553)

drawGraphWithHubs(G)

drawGiantComponent(G, 'giant')




