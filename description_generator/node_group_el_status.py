from enum import Enum


class NodeGroupElStatus(Enum):
    xor = 'xor'
    joining = 'joining'
    normal = 'normal'
    end = 'end'
