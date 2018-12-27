from enum import Enum


class NodeType(Enum):
    start_event = 'startEvent'
    sub_process = 'subProcess'
    task = 'task'
    end_event = 'endEvent'
    parallel_gateway = 'parallelGateway'
    exclusive_gateway = 'exclusiveGateway'
