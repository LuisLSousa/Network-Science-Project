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