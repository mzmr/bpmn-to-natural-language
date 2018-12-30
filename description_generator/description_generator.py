from description_generator.node_group_el_status import NodeGroupElStatus
from description_generator.node_grouper import NodeGrouper
from description_generator.node_group_el import NodeGroupEl
from description_generator.sentence.sentence_generator import SentenceGenerator
from description_generator.sentence.subject_status import SubjectStatus
from model.node import Node
from model.node_type import NodeType


class DescriptionGenerator:

    def __init__(self, node_flow: list):
        self.node_flow = node_flow
        self.generator = SentenceGenerator()

    def generate(self) -> list:
        groups = NodeGrouper(self.node_flow).group_nodes()
        sentences = [[self.__generate_sentence(el, groups) for el in gr] for gr in groups]
        DescriptionGenerator.__remove_empty_sentences(sentences)
        return sentences

    def __generate_sentence(self, group_el: NodeGroupEl, node_groups: list) -> str:
        node = self.node_flow[group_el.node_idx][0]
        predecessors = [(i, n[0]) for i, n in enumerate(self.node_flow) if group_el.node_idx in n[1]]
        successors = [(i, self.node_flow[i][0]) for i in group_el.successors_ids]
        subject_status = DescriptionGenerator.__determine_subject_status(node, predecessors)

        if node is None:  # first tuple in a list should look like (None, [start_node1, start_node2...])
            return self.generator.generate_intro_sentence([s[1] for s in successors])

        if node.type == NodeType.end_event:
            return self.generator.generate_end_sentence(node)

        if node.type == NodeType.parallel_gateway:
            if group_el.status == NodeGroupElStatus.splitting:
                return self.generator.generate_and_splitting_sentence(successors, node_groups, subject_status)

            if group_el.status == NodeGroupElStatus.normal:
                return self.generator.generate_and_joining_sentence(predecessors, node_groups, subject_status)

            if group_el.status == NodeGroupElStatus.joining:
                sentence = self.generator.generate_and_joining_sentence(predecessors, node_groups, subject_status)
                next_group_sentence = self.generator.generate_group_end_sentence(successors, node_groups)
                return f'{sentence} {next_group_sentence}'

            raise Exception()

        if node.type == NodeType.exclusive_gateway:
            if group_el.status == NodeGroupElStatus.splitting:
                return self.generator.generate_xor_splitting_sentence(node, successors, node_groups)

            if group_el.status == NodeGroupElStatus.normal:
                return self.generator.generate_xor_joining_sentence()

            if group_el.status == NodeGroupElStatus.joining:
                sentence = self.generator.generate_xor_joining_sentence()
                next_group_sentence = self.generator.generate_group_end_sentence(successors, node_groups)
                return f'{sentence} {next_group_sentence}'

            raise Exception()

        if node.type == NodeType.inclusive_gateway:
            if group_el.status == NodeGroupElStatus.splitting:
                return self.generator.generate_or_splitting_sentence(node, successors, node_groups)

            if group_el.status == NodeGroupElStatus.normal:
                return self.generator.generate_or_joining_sentence()

            if group_el.status == NodeGroupElStatus.joining:
                sentence = self.generator.generate_or_joining_sentence()
                next_group_sentence = self.generator.generate_group_end_sentence(successors, node_groups)
                return f'{sentence} {next_group_sentence}'

            raise Exception()

        if node.type == NodeType.start_event:
            return self.generator.generate_start_sentence(node, subject_status)

        if node.type == NodeType.task or node.type == NodeType.sub_process:
            is_first_in_group = False
            for group in node_groups:
                if group[0].node_idx == group_el.node_idx:
                    is_first_in_group = True
                    break

            if group_el.status == NodeGroupElStatus.joining:
                if is_first_in_group:
                    sentence = self.generator.generate_group_start_sentence(node, subject_status)
                else:
                    sentence = self.generator.generate_next_sentence(node, subject_status)

                next_group_sentence = self.generator.generate_group_end_sentence(successors, node_groups)
                return f'{sentence} {next_group_sentence}'

            if is_first_in_group:
                return self.generator.generate_group_start_sentence(node, subject_status)
            else:
                return self.generator.generate_next_sentence(node, subject_status)

        raise Exception(f'Node of type {node.type} doesn\'t fulfill any condition.')

    @staticmethod
    def __determine_subject_status(node: Node, predecessors: list) -> SubjectStatus:
        if node is None:
            return SubjectStatus.new

        if not node.lane.name:
            return SubjectStatus.none

        if len(predecessors) == 1:
            pred = predecessors[0][1]

            if pred is None:  # when the very first node is a predecessor
                return SubjectStatus.new

            if pred.type == NodeType.sub_process or pred.type == NodeType.task:
                if pred.lane.name == node.lane.name:
                    return SubjectStatus.same

        return SubjectStatus.new

    @staticmethod
    def __remove_empty_sentences(sentence_groups: list) -> None:
        for sentence_group in sentence_groups:
            for idx, sentence in enumerate(sentence_group):
                if sentence == '':
                    del sentence_group[idx]
