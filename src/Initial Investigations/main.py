import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from util import *
import pandas as pd
import scipy.stats as stats

from networkx.utils import py_random_state


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

# Logoritmic scale
# plotDegreeDistribution(degreeFrequencies, logScale=True)

# With Power law plot
# computePowerLawFitValues(degrees)
# alpha(10.43584815827752) sigma(1.308516706237002)
# loglikelihoodRatio(-0.9185063058809141) pVal(0.16159229772218375)

# drawDegreeDistributionWithPowerLaw(degrees)

# drawGraphQuantile(G)

# drawGiantComponent(G, 'giant')

drawGraphWithHubs(G)

# create one until avg path length
# nx.newman_watts_strogatz_graph(8, 4, 0.1, 5)
