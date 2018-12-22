class Node:

    def __init__(self, node_id: str):
        self.id = node_id
        self.name = ''
        self.type = ''
        self.process = ''
        self.lane = ''
        self.predecessors = []
        self.successors = []
