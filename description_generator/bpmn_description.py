from description_generator.node_group_el_status import NodeGroupElStatus
from description_generator.pojo.node_group_el import NodeGroupEl
from description_generator.sentence.sentence_generator import SentenceGenerator
from model.node_type import NodeType


class BPMNDescription:

    def __init__(self, node_flow: list):
        self.node_flow = node_flow
        self.generator = SentenceGenerator()

    def generate(self) -> list:
        groups = self.__create_node_groups()
        sentences = [[self.__generate_sentence(el, groups) for el in gr] for gr in groups]
        return sentences

    def __create_node_groups(self) -> list:
        node_groups = list()

        for idx, nf in enumerate(self.node_flow):
            self.__insert_node_into_groups(idx, nf, node_groups)

        while self.__consolidate_groups(node_groups):
            pass

        return node_groups

    def __insert_node_into_groups(self, node_idx: int, node: tuple, node_groups: list) -> None:
        successors = node[1]
        status = self.__get_group_element_status(node)
        new_group_el = NodeGroupEl(node_idx, successors, status)

        for ng in node_groups:
            for ng_el_idx, ng_el in enumerate(ng):
                if node_idx not in ng_el.successors_ids:
                    continue

                if ng_el.status == NodeGroupElStatus.normal:
                    ng.append(new_group_el)
                else:
                    node_groups.append([new_group_el])

                return

        node_groups.append([new_group_el])

    @staticmethod
    def __consolidate_groups(node_groups: list) -> bool:
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

    def __get_group_element_status(self, node: tuple) -> NodeGroupElStatus:
        successors = node[1]
        succ_number = len(successors)

        if succ_number == 0:
            return NodeGroupElStatus.end

        if succ_number > 1:
            return NodeGroupElStatus.splitting

        pred_number = len(self.node_flow[successors[0]][0].predecessors)

        if pred_number > 1:
            return NodeGroupElStatus.joining
        else:
            return NodeGroupElStatus.normal

    def __generate_sentence(self, group_el: NodeGroupEl, node_groups: list) -> str:
        node = self.node_flow[group_el.node_idx][0]
        predecessors = [(i, n[0]) for i, n in enumerate(self.node_flow) if group_el.node_idx in n[1]]
        successors = [(i, self.node_flow[i][0]) for i in group_el.successors_ids]

        if node is None:  # first tuple in a list should look like (None, [start_node1, start_node2...])
            return self.generator.generate_intro_sentence([s[1] for s in successors])

        if node.type == NodeType.end_event:
            return self.generator.generate_end_sentence()

        if node.type == NodeType.parallel_gateway:
            if group_el.status == NodeGroupElStatus.splitting:
                return self.generator.generate_and_splitting_sentence(successors, node_groups)

            if group_el.status == NodeGroupElStatus.normal:
                return self.generator.generate_and_joining_sentence(predecessors, node, node_groups)

            raise Exception()

        if node.type == NodeType.start_event:
            return self.generator.generate_start_sentence(node)

        return self.generator.generate_next_sentence(node)
