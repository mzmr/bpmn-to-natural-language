import bpmn_python.bpmn_diagram_rep as diagram
import os

from description_generator.bpmn_description import BPMNDescription
from model.bpmn_model_adapter import BPMNModelAdapter
from model.node_type import NodeType
from model.node import Node


class Translator:

    def __init__(self, filepath):
        graph = diagram.BpmnDiagramGraph()
        graph.load_diagram_from_xml_file(os.path.abspath(filepath))
        self.model_bpmn = BPMNModelAdapter(graph)

        # generowanie diagramu
        # output_directory = "./output/"
        # output_png_file = "diagram_image"
        # visualizer.bpmn_diagram_to_png(bpmn_graph, output_directory + output_png_file)

    def translate(self):
        print("Started translation...")

        start_events = self.__obtain_start_events()
        all_paths = self.__create_all_possible_node_paths(start_events)
        node_flow = self.__create_node_flow_list(all_paths)
        description = BPMNDescription(node_flow).generate()

        print("Finished translation.")
        return description

    def __obtain_start_events(self):
        return [n for n in self.model_bpmn.nodes.values() if n.type == NodeType.start_event]

    def __create_all_possible_node_paths(self, start_events: list):
        all_paths = list()

        for se in start_events:
            node_paths = self.__create_all_paths_from_node(se)
            all_paths.extend(node_paths)

        return all_paths

    @staticmethod
    def __create_all_paths_from_node(start_event: Node):
        paths = list()
        paths_temp = list()
        paths_temp.append([[], start_event])

        while paths_temp:
            current_path = paths_temp[-1]
            current_node = current_path[1]
            current_list = current_path[0]

            if current_node is None:
                paths.append(current_list)
                del paths_temp[-1]
                continue

            current_list.append(current_node)
            children = list(current_node.successors)

            if not children:
                current_path[1] = None
            else:
                current_path[1] = children.pop()

                for c in children:
                    paths_temp.append([list(current_list), c])

        return paths

    def __create_node_flow_list(self, all_paths: list):
        node_list = [n for n in self.model_bpmn.nodes.values()]
        node_list.insert(0, None)
        transition_list = [list() for _ in self.model_bpmn.nodes]
        transition_list.append(list())

        for path in all_paths:
            for node in path:
                if node.successors:
                    current_path_idx = path.index(node)
                    current_node_idx = node_list.index(node)

                    if current_path_idx == 0:
                        self.__append_if_not_in(current_node_idx, transition_list[0])

                    next_node = path[current_path_idx + 1]
                    next_node_idx = node_list.index(next_node)
                    current_node_transition = transition_list[current_node_idx]
                    self.__append_if_not_in(next_node_idx, current_node_transition)

        return list(zip(node_list, transition_list))

    @staticmethod
    def __append_if_not_in(element, the_list: list):
        if element not in the_list:
            the_list.append(element)
            return len(the_list) - 1
        else:
            return the_list.index(element)
