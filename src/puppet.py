import pandas as pd
import numpy as np
import networkx as nx
import pickle as pkl
from os.path import join
from random import choice, seed, randint
from datetime import datetime

from src.libs.visualization import *
from src.libs.graphProcessing import *
import json



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

        #pos = self.args['layout'](self.G)
        #drawGraphWithHubsV2(self.G, pos, self.args['hubPercentage'],
        #                    join(self.outputDir, 'Hubs - initial'), dpi=500)
        #exit()

        self.initialNumNodes = len(self.G.nodes())

        degreeFrequencies = np.array(nx.degree_histogram(self.G))
        degrees = [i[1] for i in self.G.degree]

        self.performAction = self.args['attackType']

        it = 0
        logs=[]

        while not self.args['stopCondition'](self.G, **self.args['stopCondArgs']):
            self.performAction(self.G, self.args['numNodesToRemove'])
            it += 1
            print('--- Outputting Iteration {} ----'.format(it))
            if it % self.args['logFreq'] == 0 or it <= self.args['initialLog']:
                print('Logging...')
                stats = calculateBasicStats(self.G)
                stats['iteration'] = it
                stats['removedPercentage'] = calcRemovedPercentage(self.G, self.initialNumNodes)
                logs.append(stats)
                # self.plots('midExecution', it)

        results = {}
        for key, val in logs[0].items():
            results[key] = []
            for l in logs:
                results[key].append(l[key])
        results = pd.DataFrame.from_dict(results)
        results.to_csv(join(self.outputDir, 'output.csv'), sep='\t', encoding='utf-8')

        with open(join(self.outputDir, 'logs.pkl'), 'wb') as f:
            pkl.dump(results, f)

        self.plots('final')



    def plots(self, type, iterator=None):
        pos = self.args['layout'](self.G)
        if type is 'midExecution':
            drawGraphWithHubs(self.G,  self.args['hubPercentage'],
                              join(self.outputDir, 'Hubs - {}'.format(iterator)))

        if type is 'final':
            '''drawGraphWithHubs(self.G, self.args['hubPercentage'],
                              join(self.outputDir, 'Hubs - final'), pos)
            '''
            drawGraphWithHubsV2(self.G, pos,  self.args['hubPercentage'],
                                join(self.outputDir, 'Hubs - {}'.format(iterator)))

            degrees = [i[1] for i in self.G.degree]
            # drawDegreeDistributionWithPowerLaw(degrees) # crashes can't plot infinity :(
            drawGiantComponent(self.G, join(self.outputDir,'giantComponent.png'), pos)

