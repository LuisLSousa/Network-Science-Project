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


def performRandFailure(G, numNodesToRemove):
    # fixme - choice
    seed(datetime.now())
    for i in range(numNodesToRemove):
        id = choice(G.nodes())
        G.remove_node(id)
    print('!! Performed Random Failure !!')

def performClusterAttack(G, numNodesToRemove):
    # if clusters are connected by a single node, remove that node
    degrees = list(G.degree())
    degreeValues = [degree for node, degree in degrees]
    degreeValues = sorted(degreeValues, reverse=False) # not used
    possibleNodes = [node for node, degree in degrees if (degree == 2 and nx.clustering(G , node) == 0) ]
    # or degree <= 3 (for example) and nx.clustering < X, with x being a number we see fit

    loopIt = numNodesToRemove if len(possibleNodes) > numNodesToRemove \
        else len(possibleNodes)

    print('Removing {} nodes'.format(loopIt))
    for i in range(loopIt):
        randIndex = choice(range(len(possibleNodes)))
        id = possibleNodes.pop(randIndex)
        print(id)
        G.remove_node(id)
    print('!! Performed Cluster Attack!!')
