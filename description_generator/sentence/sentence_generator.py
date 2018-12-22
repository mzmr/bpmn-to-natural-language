from collections import namedtuple

import morfeusz2

from description_generator.analyser_adapter import AnalyserAdapter
from description_generator.pojo.isolated_subject import AnalysedSubject
from description_generator.pojo.word_inflected import WordInflected
from description_generator.sentence.inflection_params import InflectionParams
from description_generator.sentence.sentence_database import SentenceDatabase
from model.node import Node
from utils import random_el

AnalysedPredicate = namedtuple('AnalysedPredicate', 'basic sentence_before sentence_after')


class SentenceGenerator:

    def __init__(self):
        self.morf = morfeusz2.Morfeusz()

    def generate_intro_sentence(self, start_nodes: list):
        return ''

    def generate_start_sentence(self, node: Node):
        return self.__generate_sentence(node.lane.name, node.name, SentenceDatabase.sentences_start)

    def generate_next_sentence(self, node: Node):
        return self.__generate_sentence(node.lane.name, node.name, SentenceDatabase.sentences_next)

    def generate_and_splitting_sentence(self, successors: list, node_groups: list):
        return self.__generate_splitting_sentence(successors, node_groups, SentenceDatabase.sentences_and_splitting)

    def generate_and_joining_sentence(self, node_idx: int, node: Node, node_groups: list):
        return self.__generate_joining_sentence(node_idx, node, node_groups, SentenceDatabase.sentences_and_joining)

    def generate_xor_splitting_sentence(self):
        return ''

    def generate_xor_joining_sentence(self):
        return ''

    def generate_or_splitting_sentence(self):
        return ''

    def generate_or_joining_sentence(self):
        return ''

    def generate_end_sentence(self):
        return random_el(SentenceDatabase.sentences_end)

    def __generate_sentence(self, lane_name: str, task_text: str, sentence_defs: list):
        sentence_def = random_el(sentence_defs)

        subject_analysed = self.__analyse_subject(lane_name)
        subject_inflected = self.__inflect_subject(subject_analysed.subject, sentence_def.subject_infl)

        predicate_analysed = self.__analyse_predicate(task_text)
        predicate_inflected = self.__inflect(predicate_analysed.basic, sentence_def.predicate_infl)

        result = list()
        result.append(sentence_def.text_list[0])

        if sentence_def.subject_order == 1:
            self.__append_subject(subject_inflected, subject_analysed, result)
            result.append(sentence_def.text_list[1])
            self.__append_predicate(predicate_inflected, predicate_analysed, result)
        else:
            self.__append_predicate(predicate_inflected, predicate_analysed, result)
            result.append(sentence_def.text_list[1])
            self.__append_subject(subject_inflected, subject_analysed, result)

        result.append(sentence_def.text_list[2])

        return ''.join(result)

    def __analyse_subject(self, subject: str):
        analyser = AnalyserAdapter(subject, self.morf)

        subject_forms = analyser.find_subjects()
        if subject_forms:
            sub = subject_forms[0]
        else:
            raise Exception(f'Could not find subject in "{subject}".')

        adj = None
        adjective_forms = analyser.find_adjectives(sub.params)
        if adjective_forms:
            adj = adjective_forms[0]

        gen = None
        genitive_forms = analyser.find_genitives()
        if genitive_forms:
            gen = genitive_forms[0]

        return AnalysedSubject(sub, adj, gen)

    def __analyse_predicate(self, task_text: str):
        analyser = AnalyserAdapter(task_text, self.morf)

        predicate_forms = analyser.find_predicates()
        if not predicate_forms:
            raise Exception(f'Could not find predicate in sentence: "{task_text}".')

        pre = predicate_forms[0]
        splitted_task_text = task_text.split(pre.inflected, 1)
        return AnalysedPredicate(pre.basic, splitted_task_text[0], splitted_task_text[1])

    def __inflect(self, base_word: str, inflection_params: InflectionParams):
        words = self.morf.generate(base_word)

        if len(words) == 0:
            raise ValueError(f'Unknown word: {base_word}')

        for word in words:
            if inflection_params.matches(word[2]):
                return word[0]

        raise Exception(f'Word "{base_word}" of one of types "{inflection_params.infl_params}" cannot be found.')

    @staticmethod
    def __append_subject(subject_inflected: str, subject: AnalysedSubject, result: list):
        result.append(subject_inflected)

        if subject.adjective is not None:
            result.append(' ')
            result.append(subject.adjective.inflected)

        if subject.genitive is not None:
            result.append(' ')
            result.append(subject.genitive.inflected)

    @staticmethod
    def __append_predicate(predicate_inflected: str, predicate: AnalysedPredicate, result: list):
        if predicate.sentence_before:
            result.append(predicate.sentence_before)

        result.append(predicate_inflected)

        if predicate.sentence_after:
            result.append(predicate.sentence_after)

    @staticmethod
    def __find_successor_group_idx(successor_idx: int, node_groups: list):
        for group_idx, group in enumerate(node_groups):
            if successor_idx == group[0].node_idx:
                return group_idx

        raise Exception(f'Couldn\'t find group for node with id {successor_idx}')

    def __inflect_subject(self, subject_infl: WordInflected, infl_par: InflectionParams):
        sub_infl_params = SentenceGenerator.__create_target_infl_params(subject_infl.params, infl_par)
        subject_inflected = self.__inflect(subject_infl.basic, sub_infl_params)
        return subject_inflected

    @staticmethod
    def __create_target_infl_params(src_params: str, dst_params_basic: InflectionParams):
        src_params_list = InflectionParams.inflection_str_to_list(src_params)
        gender = AnalyserAdapter.find_gender(src_params_list)
        sg_or_pl = AnalyserAdapter.find_sg_or_pl(src_params_list)
        dst_params = dst_params_basic.clone()
        dst_params.add_params(gender, sg_or_pl)
        return dst_params

    def __generate_splitting_sentence(self, successors: list, node_groups: list, sentence_defs: list):
        sentence_def = random_el(sentence_defs)

        sentence = list()
        sentence.append(sentence_def.text_list[0])

        for idx, successor in enumerate(successors):
            analysed_subject = self.__analyse_subject(successor[1].lane.name)
            inflected_subject = self.__inflect_subject(analysed_subject.subject, sentence_def.subject_infl)
            sentence.append(inflected_subject)

            if idx < len(successors) - 2:
                sentence.append(', ')
            elif idx == len(successors) - 2:
                sentence.append(' i ')

        sentence.append(sentence_def.text_list[1])

        for idx, successor in enumerate(successors):
            group_idx = SentenceGenerator.__find_successor_group_idx(successor[0], node_groups)
            sentence.append(str(group_idx))

            if idx < len(successors) - 2:
                sentence.append(', ')
            elif idx == len(successors) - 2:
                sentence.append(' oraz ')

        sentence.append(sentence_def.text_list[2])
        return ''.join(sentence)

    def __generate_joining_sentence(self, node_idx: int, node: Node, node_groups: list, sentences_defs: list):
        sentence_def = random_el(sentences_defs)

        sentence = list()
        sentence.append(sentence_def.text_list[0])

        predecessors_ids = [gr[-1].node_idx for gr in node_groups if node_idx in gr[-1].successors_ids]

        predecessors = list()
        for pred_id in predecessors_ids:
            pass


        sentence.append(sentence_def.text_list[1])

        # TODO znaleźć poprzedników gdzieś, żeby wziąć z nich nazwy podmiotów, trzeba też punkty grup, ale to chyba w pętli wcześniej

        sentence.append(sentence_def.text_list[2])

        return ''.join(sentence)
