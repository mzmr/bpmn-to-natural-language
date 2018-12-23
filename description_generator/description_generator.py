from description_generator.node_group_el_status import NodeGroupElStatus
from description_generator.node_grouper import NodeGrouper
from description_generator.pojo.node_group_el import NodeGroupEl
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

        return self.generator.generate_next_sentence(node)
