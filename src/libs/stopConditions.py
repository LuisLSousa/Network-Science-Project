import networkx as nx

def DensityStopCond(G, threshold, removedPercentage=None):
    densityThreshold = float(threshold)
    print('Calculating Density')
    density = nx.density(G)
    print('Density of {}, threshold [{}]'.format(density, threshold))
    if density < densityThreshold:
        return True
    return False


def BridgeStopCond_not_in_use(G, threshold, removedPercentage=None):
    clustersThreshold = float(threshold)
    globalClusterCoef = nx.transitivity(G)
    print('Global Cluster Coefficient of {}, threshold [{}]'.format(globalClusterCoef, threshold))
    degrees = list(G.degree())
    possibleNodes = [node for node, degree in degrees if (degree >= 2 and nx.clustering(G, node) == 0)]
    if (globalClusterCoef > clustersThreshold) or not possibleNodes:
        return True
    return False

def graphPercentageLostStopCond(G, threshold, removedPercentage):
    print('Removed Percentage of {}, threshold [{}]'.format(removedPercentage, threshold))
    if removedPercentage > threshold:
        return True
    return False

def BridgeStopCond(G, threshold, removedPercentage):
    degrees = list(G.degree())

    possibleNodes = [node for node, degree in degrees if (degree >= 2 and nx.clustering(G , node) < 0.10315322452860086) ]

    print('Removed Percentage of {}, threshold [{}]'.format(removedPercentage, threshold))
    if removedPercentage > threshold or len(possibleNodes) == 0:
        return True
    return False


