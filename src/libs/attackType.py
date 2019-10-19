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
    possibleNodes = list(G.nodes())
    for i in range(numNodesToRemove):
        randIndex = choice(range(len(possibleNodes)))
        id = possibleNodes.pop(randIndex)
        print(id)
        G.remove_node(id)
    print('!! Performed Random Failure !!')

def performBridgeAttack(G, numNodesToRemove):
    # if clusters are connected by a single node, remove that node
    degrees = list(G.degree())
    possibleNodes = [node for node, degree in degrees if (degree >= 2 and nx.clustering(G , node) == 0) ]
    # or nx.clustering < X, with x being a number we see fit
    # nx.clustering(G , node) < nx.transitivity(G)) -> we remove all nodes with a cf < global cf

    loopIt = numNodesToRemove if len(possibleNodes) > numNodesToRemove \
        else len(possibleNodes)

    print('Removing {} nodes'.format(loopIt))
    for i in range(loopIt):
        randIndex = choice(range(len(possibleNodes)))
        id = possibleNodes.pop(randIndex)
        print(id)
        G.remove_node(id)
    print('!! Performed Bridge Attack!!')

def performBetweennessAttack(G, numNodesToRemove):

    betw = nx.betweenness_centrality(G)
    betw = [(i, j) for i,j in betw.items()]

    betwValues = [i[1] for i in betw]
    betwValues = sorted(betwValues)
    possibleNodes = [node for node, btw in betw if btw == betwValues[0]]

    loopIt = numNodesToRemove if len(possibleNodes) > numNodesToRemove \
        else len(possibleNodes)

    print('Removing {} nodes'.format(loopIt))
    for i in range(loopIt):
        randIndex = choice(range(len(possibleNodes)))
        id = possibleNodes.pop(randIndex)
        print(id)
        G.remove_node(id)
    print('!! Performed Betweenness Attack !!')





