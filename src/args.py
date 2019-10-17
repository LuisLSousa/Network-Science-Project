from utils import str2bool
from src.libs.stopConditions import *


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
            ('connected elements', ConnectedElemStopCond)],
    },
]

