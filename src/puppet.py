import pandas as pd
import numpy as np
import networkx as nx
import pickle as pkl
from os.path import join
from random import choice, seed, randint
from datetime import datetime

from src.libs.visualization import *
from src.libs.graphProcessing import *


class Puppet:
    def __init__(self, args, debug, outputDir):
        """ I could pass everything from args to self right here to allow better interpretation
        of what parameters are needed fo use this class, but since we're using JARVIS that information
        can be seen in 'args.py' """
        self.args = args
        self.debug = debug
        self.outputDir = outputDir


    def pipeline(self):
        self.G = nx.read_gml(self.args['dataset'], None)
        degreeFrequencies = np.array(nx.degree_histogram(self.G))
        degrees = [i[1] for i in self.G.degree]

        if self.args['targetedAttack'] or self.args['randomFailure']:

            self.performAction = self.performTargAttack if self.args['targetedAttack'] \
                            else self.performRandFailure

            it = 0
            logs=[]

            while not self.args['stopCondition'](self.G, **self.args['stopCondArgs']):
                self.performAction()
                it += 1
                print('--- Outputting Iteration {} ----'.format(it))
                if it % self.args['logFreq'] == 0 or it <= self.args['initialLog']:
                    print('Logging...')
                    logs.append(calculateBasicStats(self.G))
                    # self.plots('midExecution', it)

            with open(join(self.outputDir, 'logs.pkl'), 'wb') as f:
                pkl.dump(logs, f)

            self.plots('final')


    def performTargAttack(self):
        degrees = list(self.G.degree())
        degreeValues = [degree for node, degree in degrees]
        degreeValues = sorted(degreeValues, reverse=True)
        possibleNodes = [node for node, degree in degrees if degree == degreeValues[0]]

        loopIt = self.args['numNodesToRemove'] if len(possibleNodes) > self.args['numNodesToRemove'] \
            else len(possibleNodes)

        print('Removing {} nodes'.format(loopIt))
        for i in range(loopIt):
            randIndex = choice(range(len(possibleNodes)))
            id = possibleNodes.pop(randIndex)
            print(id)
            self.G.remove_node(id)
        print('!! Performed Attack !!')

    def performRandFailure(self):
        # fixme - choice
        seed(datetime.now())
        for i in range(self.args['numNodesToRemove']):
            id = choice(self.G.nodes())
            self.G.remove_node(id)
        print('!! Performed Failure !!')

    def plots(self, type, iterator=None):
        if type is 'midExecution':
            drawGraphWithHubs(self.G,  self.args['hubPercentage'],
                              join(self.outputDir, 'Hubs - {}'.format(iterator)))

        if type is 'final':
            pass
