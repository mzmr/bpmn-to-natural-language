from morfeusz2 import Morfeusz

from description_generator.sentence.inflection_params import InflectionParams
from description_generator.sentence.part_of_speech_extractor import PartOfSpeechExtractor
from description_generator.sentence.pojo.sentence_def import SentenceDef


class PredicateInflector:

    def __init__(self, morfeusz: Morfeusz):
        self.morf = morfeusz

    def inflect(self, predicate_text: str, sentence_def: SentenceDef) -> str:
        return self.__inflect_predicate(predicate_text, sentence_def)

    def __inflect_predicate(self, task_text: str, sentence_def: SentenceDef) -> str:
        extractor = PartOfSpeechExtractor(task_text, self.morf)

        predicate_forms = extractor.find_predicates()
        if not predicate_forms:
            raise Exception(f'Could not find predicate in sentence: "{task_text}".')

        object_forms = extractor.find_objects()

        pred_infl = list()
        for pred in predicate_forms:
            predicate_inflected = self.__combine_params_and_inflect(pred.basic, pred.params, sentence_def.predicate_infl)
            pred_infl.append((pred.inflected, predicate_inflected))

        obj_infl = list()
        for obj in object_forms:
            object_inflected = self.__combine_params_and_inflect(obj.basic, obj.params, sentence_def.object_infl)
            obj_infl.append((obj.inflected, object_inflected))

        result = str(task_text)

        for p in pred_infl:
            result = result.replace(p[0], p[1], 1)

        for o in obj_infl:
            result = result.replace(o[0], o[1], 1)

        return result

    def __combine_params_and_inflect(self, basic_word: str, word_infl_par: str,
                                     basic_infl_par: InflectionParams) -> str:
        infl_params = PredicateInflector.__create_target_infl_params(word_infl_par, basic_infl_par)
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

    def __inflect(self, base_word: str, inflection_params: InflectionParams) -> str:
        words = self.morf.generate(base_word)

        if len(words) == 0:
            raise ValueError(f'Unknown word: {base_word}')

        for word_details in words:
            if inflection_params.matches(word_details[2]):
                return word_details[0]

        raise Exception(f'Word "{base_word}" of one of types "{inflection_params.infl_params}" cannot be found.')
