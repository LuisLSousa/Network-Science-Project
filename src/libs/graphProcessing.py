import pandas as pd
import numpy as np
import networkx as nx


def calculateBasicStats(G):
    density = nx.density(G)  # orig: 0.0005403026973346214
    globalClusteringCoef = nx.transitivity(G)  # orig: 0.10315322452860086
    if nx.is_connected(G):
        avgShortPathLen = nx.average_shortest_path_length(G)  # orig: 18.989185424445708
    # localClusteringCoefs  = nx.clustering(self.G)
    data = {k: v for k, v in locals().items()}
    del data['G']
    return data
