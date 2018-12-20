from description_generator.node_group_el_status import NodeGroupElStatus
from description_generator.pojo.node_group_el import NodeGroupEl
from description_generator.sentence.sentence_generator import SentenceGenerator
from model.node_type import NodeType


class BPMNDescription:

    def __init__(self, node_flow: list):
        self.node_flow = node_flow
        self.generator = SentenceGenerator()

    def generate(self):
        node_groups = self.__create_node_groups()
        sentences = list()

        for node in self.node_flow:
            successors = [self.node_flow[i] for i in node[1]]

            if node[0] is None:  # first tuple in a list should look like (None, [start_node1, start_node2...])
                start_nodes = [s[0] for s in successors]
                start_sentence = self.generator.generate_start_sentence(start_nodes)
                sentences.append(start_sentence)
            elif node[0].type == NodeType.end_event:
                print('endEvent node...')
            elif node[0].type == NodeType.parallel_gateway:
                print('parallelGateway node...')
            elif node[0].type == NodeType.start_event:
                print('startEvent node...')
            else:
                next_sentence = self.generator.generate_next_sentence(node[0])
                sentences.append(next_sentence)

        return sentences

    def __create_node_groups(self):
        node_groups = list()

        for idx, nf in enumerate(self.node_flow):
            self.__insert_node_into_groups(idx, nf, node_groups)

        while self.__consolidate_groups(node_groups):
            pass

        return node_groups

    def __insert_node_into_groups(self, node_idx: int, node: tuple, node_groups: list):
        successors = node[1]
        status = self.__get_group_element_status(node)
        new_group_el = NodeGroupEl(node_idx, successors, status)

        for ng in node_groups:
            for ng_el_idx, ng_el in enumerate(ng):
                if node_idx in ng_el.successors_ids:
                    if ng_el.status == NodeGroupElStatus.normal:
                        ng.append(new_group_el)
                    else:
                        node_groups.append([new_group_el])

                    return

        node_groups.append([new_group_el])

    @staticmethod
    def __consolidate_groups(node_groups: list):
        group_to_extend = None
        next_node_idx = None

        for ng in node_groups:
            last = ng[-1]

            if last.status == NodeGroupElStatus.normal:
                group_to_extend = ng
                next_node_idx = last.successors_ids[0]
                break

        if group_to_extend is None:
            return False

        ng_to_remove = None

        for ng_idx, ng in enumerate(node_groups):
            first = ng[0]

            if first.node_idx == next_node_idx:
                group_to_extend.extend(ng)
                ng_to_remove = ng_idx
                break

        if ng_to_remove is None:
            raise Exception()

        del node_groups[ng_to_remove]
        return True

    def __get_group_element_status(self, node: tuple):
        # TODO: przy tworzeniu new_group_el uzależnić status od informacji o gatewayach (jak będą zrobione)
        successors = node[1]
        succ_number = len(successors)

        if succ_number == 0:
            return NodeGroupElStatus.end

        if succ_number > 1:
            return NodeGroupElStatus.xor

        # if succ_number == 1:
        successor_idx = successors[0]
        predecessors = sum(True for n in self.node_flow if successor_idx in n[1])

        if predecessors == 1:
            return NodeGroupElStatus.normal
        else:
            return NodeGroupElStatus.joining
