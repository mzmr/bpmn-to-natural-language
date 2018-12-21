from enum import Enum


class NodeGroupElStatus(Enum):
    splitting = 'splitting'
    joining = 'joining'
    normal = 'normal'
    end = 'end'
