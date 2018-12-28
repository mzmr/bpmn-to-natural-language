import morfeusz2

from description_generator.sentence.pojo.sentence_def import SentenceDef
from description_generator.sentence.predicate_inflector import PredicateInflector
from description_generator.sentence.sentence_database import SentenceDatabase
from description_generator.sentence.subject_inflector import SubjectInflector
from description_generator.sentence.subject_status import SubjectStatus
from model.node import Node
from utils import random_el


class SentenceGenerator:

    def __init__(self):
        self.morf = morfeusz2.Morfeusz()
        self.start_was_empty = False

    def generate_intro_sentence(self, start_nodes: list) -> str:
        if len(start_nodes) == 1:
            return random_el(SentenceDatabase.sentences_intro_single)
        else:
            return ''

    def generate_start_sentence(self, node: Node, subject_status: SubjectStatus) -> str:
        if node.name:
            if subject_status == SubjectStatus.none:
                return self.__generate_sentence(node.lane.name, node.name, SentenceDatabase.sentences_start_no_subject)
            else:
                return self.__generate_sentence(node.lane.name, node.name, SentenceDatabase.sentences_start)
        else:
            self.start_was_empty = True
            return ''

    def generate_next_sentence(self, node: Node, subject_status: SubjectStatus) -> str:
        if self.start_was_empty:
            self.start_was_empty = False
            return self.generate_start_sentence(node, subject_status)

        sentence_defs = None

        if subject_status == SubjectStatus.new:
            sentence_defs = SentenceDatabase.sentences_next
        elif subject_status == SubjectStatus.same:
            sentence_defs = SentenceDatabase.sentences_next_default_subject
        elif subject_status == SubjectStatus.none:
            sentence_defs = SentenceDatabase.sentences_next_no_subject

        return self.__generate_sentence(node.lane.name, node.name, sentence_defs)

    def generate_and_splitting_sentence(self, successors: list, node_groups: list,
                                        subject_status: SubjectStatus) -> str:
        if subject_status == SubjectStatus.none:
            return self.__generate_split_or_join_sentence_no_subject(
                successors, node_groups, SentenceDatabase.sentences_and_splitting_no_subject)
        else:
            return self.__generate_split_or_join_sentence(successors, node_groups,
                                                          SentenceDatabase.sentences_and_splitting)

    def generate_and_joining_sentence(self, predecessors: list, node_groups: list,
                                      subject_status: SubjectStatus) -> str:
        if subject_status == SubjectStatus.none:
            return self.__generate_split_or_join_sentence_no_subject(
                predecessors, node_groups, SentenceDatabase.sentences_and_joining_no_subject)
        else:
            return self.__generate_split_or_join_sentence(predecessors, node_groups,
                                                          SentenceDatabase.sentences_and_joining)

    def generate_xor_splitting_sentence(self, node: Node, successors: list, node_groups: list,
                                        subject_status: SubjectStatus) -> str:
        return self.__generate_split_choice_sentence(node, successors, node_groups,
                                                     SentenceDatabase.sentences_xor_splitting)

    def generate_xor_joining_sentence(self, predecessors: list, node_groups: list) -> str:
        return random_el(SentenceDatabase.sentences_xor_joining)

    def generate_or_splitting_sentence(self, successors: list, node_groups: list) -> str:
        return ''

    def generate_or_joining_sentence(self, predecessors: list, node_groups: list) -> str:
        return ''

    def generate_end_sentence(self) -> str:
        return random_el(SentenceDatabase.sentences_end)

    def generate_group_end_sentence(self, successors: list, node_groups: list) -> str:
        sentence_def_tuple = random_el(SentenceDatabase.sentences_group_end)

        succ_id = successors[0][0]  # should be only one when joining

        for group_idx, group in enumerate(node_groups):
            for el in group:
                if el.node_idx == succ_id:
                    return f'{sentence_def_tuple[0]}{group_idx + 1}{sentence_def_tuple[1]}'

        raise Exception()

    def generate_group_start_sentence(self, node: Node, subject_status: SubjectStatus):
        if subject_status == SubjectStatus.none:
            return self.__generate_sentence(node.lane.name, node.name,
                                            SentenceDatabase.sentences_group_start_no_subject)
        else:
            return self.__generate_sentence(node.lane.name, node.name, SentenceDatabase.sentences_group_start)

    def __generate_sentence(self, lane_name: str, task_text: str, sentence_defs: list) -> str:
        sentence_def = random_el(sentence_defs)

        if not lane_name:
            return self.__generate_sentence_no_subject(task_text, sentence_def)

        if sentence_def.subject_infl is None:
            return self.__generate_sentence_no_subject(task_text, sentence_def)
        else:
            return self.__generate_sentece_regular(lane_name, task_text, sentence_def)

    @staticmethod
    def __find_successor_group_idx(successor_idx: int, node_groups: list) -> int:
        for group_idx, group in enumerate(node_groups):
            for el in group:
                if successor_idx == el.node_idx:
                    return group_idx

        raise Exception(f'Couldn\'t find group for node with id {successor_idx}')

    def __generate_split_or_join_sentence(self, nodes: list, node_groups: list, sentence_defs: list) -> str:
        sentence_def = random_el(sentence_defs)

        sentence = list()
        sentence.append(sentence_def.text_list[0])
        nodes_subjects = [s[1].lane.name for s in nodes]
        sentence.append(self.__list_inflected_subjects(nodes_subjects, sentence_def))
        sentence.append(sentence_def.text_list[1])
        succ_ids = [s[0] for s in nodes]
        sentence.append(SentenceGenerator.__list_points(succ_ids, node_groups))
        sentence.append(sentence_def.text_list[2])
        return ''.join(sentence)

    def __generate_split_or_join_sentence_no_subject(self, nodes: list, node_groups: list, sentence_defs: list) -> str:
        sentence_def = random_el(sentence_defs)

        sentence = list()
        sentence.append(sentence_def[0])
        succ_ids = [s[0] for s in nodes]
        sentence.append(SentenceGenerator.__list_points(succ_ids, node_groups))
        sentence.append(sentence_def[1])
        return ''.join(sentence)

    def __list_inflected_subjects(self, subjects: list, sentence_def: SentenceDef) -> str:
        infl_subs = list()

        for idx, subject in enumerate(subjects):
            sub_infl = SubjectInflector(self.morf).inflect(subject, sentence_def)
            infl_subs.append(SentenceGenerator.__word_with_comma(sub_infl, idx, subjects))

        return ''.join(infl_subs)

    @staticmethod
    def __list_points(nodes_ids: list, node_groups: list) -> str:
        points = list()

        for idx, node_id in enumerate(nodes_ids):
            group_idx = SentenceGenerator.__find_successor_group_idx(node_id, node_groups)
            points.append(SentenceGenerator.__word_with_comma(str(group_idx + 1), idx, nodes_ids))

        return ''.join(points)

    @staticmethod
    def __word_with_comma(word: str, idx: int, word_list: list) -> str:
        conj = random_el(['i', 'oraz'])

        if idx < len(word_list) - 2:
            return f'{word}, '
        elif idx == len(word_list) - 2:
            return f'{word} {conj} '
        else:
            return word

    def __generate_sentence_no_subject(self, task_text: str, sentence_def: SentenceDef):
        pred = PredicateInflector(self.morf).inflect(task_text, sentence_def)
        result = list()
        result.append(sentence_def.text_list[0])
        result.append(pred)
        result.append(sentence_def.text_list[1])

        return ''.join(result)

    def __generate_sentece_regular(self, lane_name: str, task_text: str, sentence_def: SentenceDef):
        sub = SubjectInflector(self.morf).inflect(lane_name, sentence_def)
        pred = PredicateInflector(self.morf).inflect(task_text, sentence_def)

        result = list()
        result.append(sentence_def.text_list[0])

        if sentence_def.subject_order == 1:
            result.append(sub)
            result.append(sentence_def.text_list[1])
            result.append(pred)
        else:
            result.append(pred)
            result.append(sentence_def.text_list[1])
            result.append(sub)

        result.append(sentence_def.text_list[2])

        return ''.join(result)

    def __generate_split_choice_sentence(self, node: Node, successors: list, node_groups: list, sentence_defs: list):
        sentence_def = random_el(sentence_defs)

        sentence = list()
        question = SentenceGenerator.__prepare_question(node.name)
        sentence.append(question)

        for arr_text, successor in node.arrows_outgoing:
            sentence.append(' Jeśli ')
            sentence.append(arr_text.lower())
            sentence.append(sentence_def[0])

            succ_idx = None
            for idx, s in successors:
                if s == successor:
                    succ_idx = idx
                    break
            if succ_idx is None:
                raise Exception()

            group_idx = SentenceGenerator.__find_successor_group_idx(succ_idx, node_groups)

            sentence.append(str(group_idx + 1))
            sentence.append(sentence_def[1])

        sentence.append(sentence_def[2])

        return ''.join(sentence)

    @staticmethod
    def __prepare_question(basic_question: str) -> str:
        if basic_question.endswith('?'):
            question = basic_question
        else:
            question = basic_question + '?'

        return question.capitalize()
