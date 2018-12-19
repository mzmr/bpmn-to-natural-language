from bpmn_python.bpmn_diagram_rep import BpmnDiagramGraph

from model.node_type import NodeType
from model.node import Node
from collections import namedtuple
Lane = namedtuple('Lane', 'id name')
Process = namedtuple('Process', 'id name')


class BPMNModelAdapter:

    def __init__(self, bpmn_diagram: BpmnDiagramGraph):
        self.nodes = dict()
        self.__remodel_diagram(bpmn_diagram)

    def __remodel_diagram(self, bpmn_diagram: BpmnDiagramGraph):
        self.__create_node_list(bpmn_diagram.sequence_flows)
        self.__complete_node_params(bpmn_diagram.diagram_graph.node)
        self.__complete_lanes_and_processes(bpmn_diagram.process_elements)

    def __create_node_list(self, sequence_flows: dict):
        for flow in sequence_flows.values():
            node_src_id = flow['sourceRef']
            node_dst_id = flow['targetRef']

            node_src = self.__add_if_not_exist(node_src_id)
            node_dst = self.__add_if_not_exist(node_dst_id)

            if node_dst not in node_src.successors:
                node_src.successors.append(node_dst)

    def __complete_node_params(self, nodes: dict):
        for n in nodes.values():
            node = self.nodes[n['id']]
            node.name = n['node_name']
            node.type = NodeType(n['type'])

    def __complete_lanes_and_processes(self, process_elements: dict):
        for p in process_elements.values():
            for lane in p['laneSet']['lanes'].values():
                for n in lane['flowNodeRefs']:
                    self.nodes[n].lane = Lane(lane['id'], lane['name'])
                    self.nodes[n].process = Process(p['id'], p['name'])

    def __add_if_not_exist(self, node_id: str):
        if not node_id:
            raise ValueError('node_id cannot be empty')
        if node_id in self.nodes:
            return self.nodes[node_id]

        new_node = Node(node_id)
        self.nodes[node_id] = new_node
        return new_node
