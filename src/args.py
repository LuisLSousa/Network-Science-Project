from utils import str2bool
from src.libs.stopConditions import *
from src.libs.attackType import *
import networkx as nx

argListPuppet = [
    {
        'name': 'dataset',
        'type': str,
        'default': False,
        'required': True,
        'help': '[String] Dataset path',
    },
    {
        'name': 'randomFailure',
        'type': str2bool,
        'default': False,
        'required': False,
        'help': '[Bool] Pipeline config',
    },
    {
        'name': 'targetedAttack',
        'type': str2bool,
        'default': False,
        'required': False,
        'help': '[Bool] Pipeline config',
    },
    {
        'name': 'stopCondition',
        'type': str,
        'default': None,
        'required': True,
        'help': '[String] When to stop performing actions to the graph',
        'possibilities': [
            ('density', DensityStopCond),
            ('clusters', ClustersStopCond),
            ('lostPercentage', graphPercentageLostStopCond)],
    },
    {
        'name': 'attackType',
        'type': str,
        'default': None,
        'required': True,
        'help': '[String] The action to perform to the graph',
        'possibilities': [
            ('hubs', performHubAttack),
            ('random', performRandFailure),
            ('bridge',performBridgeAttack),
            ('betweenness', performBetweennessAttack)],
    },
    {
        'name': 'layout',
        'type': str,
        'default': None,
        'required': True,
        'help': '[String] Layout of graph plots',
        'possibilities': [
            ('spring', nx.spring_layout),
            ('spectral', nx.spectral_layout),
            ('shell', nx.shell_layout),]
    },
]

