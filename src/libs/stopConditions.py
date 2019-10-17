import networkx as nx

def DensityStopCond(G, threshold):
    densityThreshold = float(threshold)
    print('Calculating Density')
    density = nx.density(G)
    print('Density of {}, threshold [{}]'.format(density, threshold))
    if density < densityThreshold:
        return True
    return False

def ConnectedElemStopCond(G, numElements):
    pass

def ClustersStopCond(G, threshold):
    clustersThreshold = float (threshold)
    globalClusterCoef = nx.transitivity(G)
    print('Global Cluster Coefficient of {}, threshold [{}]'.format(globalClusterCoef, threshold))
    if globalClusterCoef > clustersThreshold:
        return True
    return False
