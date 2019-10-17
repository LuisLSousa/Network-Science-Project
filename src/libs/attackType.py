from random import choice, seed, randint
from datetime import datetime

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
    print('!! Performed Attack !!')


def performRandFailure(G, numNodesToRemove):
    # fixme - choice
    seed(datetime.now())
    for i in range(numNodesToRemove):
        id = choice(G.nodes())
        G.remove_node(id)
    print('!! Performed Failure !!')
