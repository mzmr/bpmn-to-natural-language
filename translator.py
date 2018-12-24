from description_generator.description_generator import DescriptionGenerator
from model.bpmn_model_adapter import BPMNModelAdapter
from model.node_type import NodeType
from model.node import Node
from utils import append_if_not_in


class Translator:

    def __init__(self, filepath):
        self.model_bpmn = BPMNModelAdapter(filepath)

        # generowanie diagramu
        # output_directory = "./output/"
        # output_png_file = "diagram_image"
        # visualizer.bpmn_diagram_to_png(bpmn_graph, output_directory + output_png_file)

    def translate(self) -> list:
        print("Started translation...")

        start_events = self.__obtain_start_events()
        all_paths = self.__create_all_possible_node_paths(start_events)
        node_flow = self.__create_node_flow_list(all_paths)
        description = DescriptionGenerator(node_flow).generate()

        print("Finished translation.")
        return description

    def __obtain_start_events(self) -> list:
        return [n for n in self.model_bpmn.nodes.values() if n.type == NodeType.start_event]

    def __create_all_possible_node_paths(self, start_events: list) -> list:
        paths_lists = [self.__create_all_paths_from_node(start) for start in start_events]
        return [p for paths in paths_lists for p in paths]

    @staticmethod
    def __create_all_paths_from_node(start_event: Node) -> list:
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
            children = current_node.successors.copy()

            if not children:
                current_path[1] = None
            else:
                current_path[1] = children.pop()
                paths_temp.extend([[current_list.copy(), c] for c in children])

        return paths

    def __create_node_flow_list(self, all_paths: list) -> list:
        node_list = list(self.model_bpmn.nodes.values())
        node_list.insert(0, None)
        transition_list = [list() for _ in range(len(self.model_bpmn.nodes) + 1)]

        for path in all_paths:
            for current_path_idx, node in enumerate(path):
                if not node.successors:
                    continue

                current_node_idx = node_list.index(node)

                if current_path_idx == 0:
                    append_if_not_in(current_node_idx, transition_list[0])

                next_node = path[current_path_idx + 1]
                next_node_idx = node_list.index(next_node)
                current_node_transition = transition_list[current_node_idx]
                append_if_not_in(next_node_idx, current_node_transition)

        return list(zip(node_list, transition_list))
