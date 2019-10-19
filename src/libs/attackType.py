from random import choice, seed, randint
from datetime import datetime
import networkx as nx

def performHubAttack(G, numNodesToRemove):
    degrees = list(G.degree())
    degreeValues = [degree for node, degree in degrees]
    degreeValues = sorted(degreeValues, reverse=True)
    possibleNodes = [node for node, degree in degrees if degree == degreeValues[0]]

    loopIt = numNodesToRemove if len(possibleNodes) > numNodesToRemove \
        else len(possibleNodes)

    print('Removing {} nodes'.format(loopIt))
    for i in range(loopIt):
        randIndex = choice(range(len(possibleNodes)))
        id = possibleNodes.pop(randIndex)
        print(id)
        G.remove_node(id)
    print('!! Performed Hubs Attack !!')
    return loopIt


def performRandFailure(G, numNodesToRemove):
    # fixme - choice
    seed(datetime.now())
    possibleNodes = list(G.nodes())
    for i in range(numNodesToRemove):
        randIndex = choice(range(len(possibleNodes)))
        id = possibleNodes.pop(randIndex)
        print(id)
        G.remove_node(id)
    print('!! Performed Random Failure !!')
    return numNodesToRemove


def performClustersAttack(G, numNodesToRemove):
    # if clusters are connected by a single node, remove that node
    degrees = list(G.degree())
    possibleNodes = [node for node, degree in degrees if (degree >= 2 and nx.clustering(G , node)==0) ]
    # or nx.clustering < X, with x being a number we see fit. Original global cf = 0.10315322452860086
    # nx.clustering(G , node) < nx.transitivity(G)) -> we remove all nodes with a cf < global cf - takes a lot to compute

    loopIt = numNodesToRemove if len(possibleNodes) > numNodesToRemove \
        else len(possibleNodes)

    print('Removing {} nodes'.format(loopIt))
    for i in range(loopIt):
        randIndex = choice(range(len(possibleNodes)))

        id = possibleNodes.pop(randIndex)
        print(id)
        G.remove_node(id)
    return loopIt

    print('!! Performed Bridge Attack!!')


def performBridgeAttack(G, numNodesToRemove):
    # if clusters are connected by a single node, remove that node
    degrees = list(G.degree())
    possibleNodes = [node for node, degree in degrees if (degree >= 2 and nx.clustering(G , node) < 0.10315322452860086) ]
    # or nx.clustering < X, with x being a number we see fit. Original global cf = 0.10315322452860086
    # nx.clustering(G , node) < nx.transitivity(G)) -> we remove all nodes with a cf < global cf - takes a lot to compute

    loopIt = numNodesToRemove if len(possibleNodes) > numNodesToRemove \
        else len(possibleNodes)

    print('Removing {} nodes'.format(loopIt))
    for i in range(loopIt):
        randIndex = choice(range(len(possibleNodes)))

        id = possibleNodes.pop(randIndex)
        print(id)
        G.remove_node(id)
    return loopIt
    print('!! Performed Bridge Attack!!')

def performBetweennessAttack(G, numNodesToRemove):

    betw = nx.betweenness_centrality(G)
    betw = [(i, j) for i, j in betw.items()]

    betwValues = sorted(betw, reverse=True, key=lambda x: x[1])
    possibleNodes = [node for node, value in betwValues]
    '''
    loopIt = numNodesToRemove if len(possibleNodes) > numNodesToRemove \
        else len(possibleNodes)
    '''
    if numNodesToRemove > len(possibleNodes):
        print('Removing {} nodes'.format(numNodesToRemove))
        for i in range(numNodesToRemove):
            id = possibleNodes[i]
            print(id)
            G.remove_node(id)
        print('!! Performed Betweenness Attack !!')
        return numNodesToRemove
    else:
        print('Caanot remove more node...')
        return 0
