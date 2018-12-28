import morfeusz2

from description_generator.sentence.part_of_speech_extractor import PartOfSpeechExtractor
from description_generator.sentence.pojo.extracted_predicate import ExtractedPredicate
from description_generator.sentence.pojo.extracted_subject import ExtractedSubject
from description_generator.sentence.inflection_params import InflectionParams
from description_generator.sentence.pojo.sentence_def import SentenceDef
from description_generator.sentence.sentence_database import SentenceDatabase
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
        return self.__generate_split_choice_sentence(node, successors, node_groups, SentenceDatabase.sentences_xor_splitting)

    def generate_xor_joining_sentence(self, predecessors: list, node_groups: list) -> str:
        return ''

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

    def __extract_subject(self, subject: str) -> ExtractedSubject:
        extractor = PartOfSpeechExtractor(subject.lower(), self.morf)

        subject_forms = extractor.find_subjects()
        if subject_forms:
            sub = subject_forms[0]
        else:
            raise Exception(f'Could not find subject in "{subject}".')

        adj = None
        adjective_forms = extractor.find_adjectives(sub.params)
        if adjective_forms:
            adj = adjective_forms[0]

        gen = None
        genitive_forms = extractor.find_genitives()
        if genitive_forms:
            gen = genitive_forms[0]

        return ExtractedSubject(sub, adj, gen)

    def __extract_predicate(self, task_text: str) -> ExtractedPredicate:
        extractor = PartOfSpeechExtractor(task_text, self.morf)

        predicate_forms = extractor.find_predicates()
        if predicate_forms:
            pre = predicate_forms[0]
        else:
            raise Exception(f'Could not find predicate in sentence: "{task_text}".')

        obj = None
        object_forms = extractor.find_objects()
        if object_forms:
            obj = object_forms[0]

        splitted_task_text = task_text.split(pre.inflected, 1)
        splitted_second = splitted_task_text[1].split(obj.inflected, 1)
        splitted = [splitted_task_text[0], splitted_second[0], splitted_second[1]]
        return ExtractedPredicate(pre, obj, splitted)

    def __inflect(self, base_word: str, inflection_params: InflectionParams) -> str:
        words = self.morf.generate(base_word)

        if len(words) == 0:
            raise ValueError(f'Unknown word: {base_word}')

        for word_details in words:
            if inflection_params.matches(word_details[2]):
                return word_details[0]

        raise Exception(f'Word "{base_word}" of one of types "{inflection_params.infl_params}" cannot be found.')

    @staticmethod
    def __append_subject(subject_inflected: str, subject: ExtractedSubject, result: list) -> None:
        result.append(subject_inflected)

        if subject.adjective is not None:
            result.append(' ')
            result.append(subject.adjective.inflected)

        if subject.genitive is not None:
            result.append(' ')
            result.append(subject.genitive.inflected)

    @staticmethod
    def __append_predicate(pred_infl: str, obj_infl: str, predicate: ExtractedPredicate, result: list) -> None:
        if predicate.sentence_parts[0]:
            result.append(predicate.sentence_parts[0])

        result.append(pred_infl)

        if predicate.sentence_parts[1]:
            result.append(predicate.sentence_parts[1])

        result.append(obj_infl)

        if predicate.sentence_parts[2]:
            result.append(predicate.sentence_parts[2])

    @staticmethod
    def __find_successor_group_idx(successor_idx: int, node_groups: list) -> int:
        for group_idx, group in enumerate(node_groups):
            for el in group:
                if successor_idx == el.node_idx:
                    return group_idx

        raise Exception(f'Couldn\'t find group for node with id {successor_idx}')

    def __combine_params_and_inflect(self, basic_word: str, word_infl_par: str,
                                     basic_infl_par: InflectionParams) -> str:
        infl_params = SentenceGenerator.__create_target_infl_params(word_infl_par, basic_infl_par)
        word_inflected = self.__inflect(basic_word, infl_params)
        return word_inflected

    @staticmethod
    def __create_target_infl_params(src_params: str, dst_params_basic: InflectionParams) -> InflectionParams:
        src_params_list = InflectionParams.inflection_str_to_list(src_params)
        gender = PartOfSpeechExtractor.find_gender(src_params_list)
        sg_or_pl = PartOfSpeechExtractor.find_sg_or_pl(src_params_list)
        dst_params = dst_params_basic.clone()

        if gender:
            dst_params.add_params(gender, sg_or_pl)
        else:
            dst_params.add_param(sg_or_pl)

        return dst_params

    def __generate_split_or_join_sentence(self, nodes: list, node_groups: list, sentence_defs: list) -> str:
        sentence_def = random_el(sentence_defs)

        sentence = list()
        sentence.append(sentence_def.text_list[0])
        nodes_subjects = [s[1].lane.name for s in nodes]
        sentence.append(self.__list_inflected_subjects(nodes_subjects, sentence_def.subject_infl))
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

    def __list_inflected_subjects(self, subjects: list, subject_infl: InflectionParams) -> str:
        infl_subs = list()

        for idx, subject in enumerate(subjects):
            subject_extracted = self.__extract_subject(subject)
            subject_inflected = self.__combine_params_and_inflect(subject_extracted.subject.basic,
                                                                  subject_extracted.subject.params,
                                                                  subject_infl)
            infl_subs.append(SentenceGenerator.__word_with_comma(subject_inflected, idx, subjects))

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
        predicate_extracted = self.__extract_predicate(task_text)
        predicate_inflected = self.__combine_params_and_inflect(predicate_extracted.predicate.basic,
                                                                predicate_extracted.predicate.params,
                                                                sentence_def.predicate_infl)
        object_inflected = self.__combine_params_and_inflect(predicate_extracted.object.basic,
                                                             predicate_extracted.object.params,
                                                             sentence_def.object_infl)

        result = list()
        result.append(sentence_def.text_list[0])

        self.__append_predicate(predicate_inflected, object_inflected, predicate_extracted, result)
        result.append(sentence_def.text_list[1])

        return ''.join(result)

    def __generate_sentece_regular(self, lane_name: str, task_text: str, sentence_def: SentenceDef):
        subject_extracted = self.__extract_subject(lane_name)
        subject_inflected = self.__combine_params_and_inflect(subject_extracted.subject.basic,
                                                              subject_extracted.subject.params,
                                                              sentence_def.subject_infl)

        predicate_extracted = self.__extract_predicate(task_text)
        predicate_inflected = self.__combine_params_and_inflect(predicate_extracted.predicate.basic,
                                                                predicate_extracted.predicate.params,
                                                                sentence_def.predicate_infl)
        object_inflected = self.__combine_params_and_inflect(predicate_extracted.object.basic,
                                                             predicate_extracted.object.params,
                                                             sentence_def.object_infl)

        result = list()
        result.append(sentence_def.text_list[0])

        if sentence_def.subject_order == 1:
            self.__append_subject(subject_inflected, subject_extracted, result)
            result.append(sentence_def.text_list[1])
            self.__append_predicate(predicate_inflected, object_inflected, predicate_extracted, result)
        else:
            self.__append_predicate(predicate_inflected, object_inflected, predicate_extracted, result)
            result.append(sentence_def.text_list[1])
            self.__append_subject(subject_inflected, subject_extracted, result)

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
