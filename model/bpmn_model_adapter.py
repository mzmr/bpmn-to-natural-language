import bpmn_python.bpmn_diagram_rep as diagram
import os

from model.node_type import NodeType
from model.node import Node
from collections import namedtuple
Lane = namedtuple('Lane', 'id name')
Process = namedtuple('Process', 'id name')


class BPMNModelAdapter:

    def __init__(self, filepath: str):
        self.nodes = dict()
        graph = diagram.BpmnDiagramGraph()
        graph.load_diagram_from_xml_file(os.path.abspath(filepath))
        self.__remodel_diagram(graph)

    def __remodel_diagram(self, bpmn_diagram: diagram.BpmnDiagramGraph) -> None:
        self.__create_node_list(bpmn_diagram.sequence_flows)
        self.__complete_node_params(bpmn_diagram.diagram_graph.node)
        self.__complete_lanes_and_processes(bpmn_diagram.process_elements)

    def __create_node_list(self, sequence_flows: dict) -> None:
        for flow in sequence_flows.values():
            node_src_id = flow['sourceRef']
            node_dst_id = flow['targetRef']

            node_src = self.__add_if_not_exist(node_src_id)
            node_dst = self.__add_if_not_exist(node_dst_id)

            if node_dst not in node_src.successors:
                node_src.successors.append(node_dst)

            if node_src not in node_dst.predecessors:
                node_dst.predecessors.append(node_src)

    def __complete_node_params(self, nodes: dict) -> None:
        for n in nodes.values():
            node = self.nodes[n['id']]
            node.name = n['node_name']
            node.type = NodeType(n['type'])

    def __complete_lanes_and_processes(self, process_elements: dict) -> None:
        for p in process_elements.values():
            process = Process(p['id'], p['name'])

            for l in p['laneSet']['lanes'].values():
                lane = Lane(l['id'], l['name'])

                for n in l['flowNodeRefs']:
                    self.nodes[n].lane = lane
                    self.nodes[n].process = process

    def __add_if_not_exist(self, node_id: str) -> Node:
        if not node_id:
            raise ValueError('node_id cannot be empty')
        if node_id in self.nodes:
            return self.nodes[node_id]

        new_node = Node(node_id)
        self.nodes[node_id] = new_node
        return new_node
