from utils import str2bool
from src.libs.stopConditions import *
from src.libs.attackType import *


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
            ('connected elements', ConnectedElemStopCond),
            ('clusters', ClustersStopCond)],
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
            ('clusters',performClusterAttack)],
    },
]

