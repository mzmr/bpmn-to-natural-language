from description_generator.node_group_el_status import NodeGroupElStatus
from description_generator.node_grouper import NodeGrouper
from description_generator.node_group_el import NodeGroupEl
from description_generator.sentence.sentence_generator import SentenceGenerator
from model.node_type import NodeType


class DescriptionGenerator:

    def __init__(self, node_flow: list):
        self.node_flow = node_flow
        self.generator = SentenceGenerator()

    def generate(self) -> list:
        groups = NodeGrouper(self.node_flow).group_nodes()
        sentences = [[self.__generate_sentence(el, groups) for el in gr] for gr in groups]
        return sentences

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
                return self.generator.generate_and_joining_sentence(predecessors, node_groups)

            raise Exception()

        if node.type == NodeType.start_event:
            return self.generator.generate_start_sentence(node)

        if node.type == NodeType.task or node.type == NodeType.sub_process:
            is_first_in_group = False
            for group in node_groups:
                if group[0].node_idx == group_el.node_idx:
                    is_first_in_group = True
                    break

            is_the_same_subject = False
            if len(predecessors) == 1:
                pred = predecessors[0][1]

                if pred.type == NodeType.sub_process or pred.type == NodeType.task:
                    pred_sub = pred.lane.name
                    my_sub = node.lane.name
                    is_the_same_subject = pred_sub == my_sub

            if group_el.status == NodeGroupElStatus.joining:
                if is_first_in_group:
                    sentence = self.generator.generate_group_start_sentence(node)
                else:
                    sentence = self.generator.generate_next_sentence(node, is_the_same_subject)

                next_group_sentence = self.generator.generate_group_end_sentence(successors, node_groups)
                return f'{sentence} {next_group_sentence}'

            if is_first_in_group:
                return self.generator.generate_group_start_sentence(node)
            else:
                return self.generator.generate_next_sentence(node, is_the_same_subject)

        raise Exception()
