from collections import namedtuple
from random import randint

import morfeusz2

from description_generator.analyser_adapter import AnalyserAdapter
from description_generator.pojo.isolated_subject import IsolatedSubject
from description_generator.sentence.inflection_params import InflectionParams
from description_generator.sentence.sentence_database import SentenceDatabase

IsolatedPredicate = namedtuple('IsolatedPredicate', 'basic sentence_before sentence_after')


class SentenceGenerator:

    def __init__(self):
        self.morf = morfeusz2.Morfeusz()

    def generate_start_sentence(self, start_nodes: list):
        if len(start_nodes) == 1:
            return self.__generate_sentence(start_nodes[0].lane.name,
                                            start_nodes[0].name,
                                            SentenceDatabase.sentences_start)
        else:
            return self.__generate_multiple_node_sentence(start_nodes, SentenceDatabase.sentences_start)

    def __generate_sentence(self, lane_name: str, task_text: str, sentence_defs: list):
        sentence_def = SentenceDatabase.sentences_start[randint(0, len(sentence_defs) - 1)]
        subject_isolated = self.__isolate_subject(lane_name)  # zmienić na __retrieve_subject
        predicate = self.__isolate_predicate(task_text)

        subject_params = InflectionParams.inflection_str_to_list(subject_isolated.subject.params)
        subject_gender = AnalyserAdapter.find_gender(subject_params)
        subject_sg_or_pl = AnalyserAdapter.find_sg_or_pl(subject_params)
        sub_infl_params = sentence_def.subject_infl.clone()
        sub_infl_params.add_param(subject_gender)
        sub_infl_params.add_param(subject_sg_or_pl)
        subject_inflected = self.__inflect(subject_isolated.subject.basic, sub_infl_params)

        predicate_inflected = self.__inflect(predicate.basic, sentence_def.predicate_infl)

        result = list()
        result.append(sentence_def.text_list[0])

        if sentence_def.subject_order == 1:
            self.__append_subject(subject_inflected, subject_isolated, result)
            result.append(sentence_def.text_list[1])
            self.__append_predicate(predicate_inflected, predicate, result)
        else:
            self.__append_predicate(predicate_inflected, predicate, result)
            result.append(sentence_def.text_list[1])
            self.__append_subject(subject_inflected, subject_isolated, result)

        result.append(sentence_def.text_list[2])

        # while '' in result:
        #     result.remove('')
        #
        # while None in result:
        #     result.remove(None)

        return ''.join(result)

    def __isolate_subject(self, subject: str):
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

        return IsolatedSubject(sub, adj, gen)

    def __isolate_predicate(self, task_text: str):
        analyser = AnalyserAdapter(task_text, self.morf)

        predicate_forms = analyser.find_predicates()
        if not predicate_forms:
            raise Exception(f'Could not find predicate in sentence: "{task_text}".')

        pre = predicate_forms[0]
        splitted_task_text = task_text.split(pre.inflected, 1)
        return IsolatedPredicate(pre.basic, splitted_task_text[0], splitted_task_text[1])

    def __inflect(self, base_word: str, inflection_params: InflectionParams):
        words = self.morf.generate(base_word)

        if len(words) == 0:
            raise ValueError(f'Unknown word: {base_word}')

        for word in words:
            if inflection_params.matches(word[2]):
                return word[0]

        raise Exception(f'Word "{base_word}" of one of types "{inflection_params.infl_params}" cannot be found.')

    def __generate_multiple_node_sentence(self, start_nodes: list, sentences_defs: list):
        pass

    @staticmethod
    def __append_subject(subject_inflected: str, subject: IsolatedSubject, result: list):
        result.append(subject_inflected)

        if subject.adjective is not None:
            result.append(' ')
            result.append(subject.adjective.inflected)

        if subject.genitive is not None:
            result.append(' ')
            result.append(subject.genitive.inflected)

    @staticmethod
    def __append_predicate(predicate_inflected: str, predicate: IsolatedPredicate, result: list):
        if predicate.sentence_before:
            result.append(predicate.sentence_before)

        result.append(predicate_inflected)

        if predicate.sentence_after:
            result.append(predicate.sentence_after)
