from morfeusz2 import Morfeusz

from description_generator.sentence.inflection_params import InflectionParams
from description_generator.sentence.inflector import Inflector
from description_generator.sentence.part_of_speech_extractor import PartOfSpeechExtractor
from description_generator.sentence.pojo.sentence_def import SentenceDef


class PredicateInflector(Inflector):

    def __init__(self, morfeusz: Morfeusz):
        Inflector.__init__(self, morfeusz)

    def inflect(self, predicate_text: str, sentence_def: SentenceDef) -> str:
        extractor = PartOfSpeechExtractor(predicate_text, self.morf)

        predicate_forms = extractor.find_predicates()
        if not predicate_forms:
            raise ValueError(f'Could not find predicate in sentence: "{predicate_text}".')

        object_forms = extractor.find_objects()
        participle_forms = extractor.find_participles()
        obj_adjective_forms = extractor.find_obj_adjectives()

        pred_infl = self.__inflect_forms(predicate_forms, sentence_def.predicate_infl)
        part_params = InflectionParams('ppas', sentence_def.object_infl.get_grammatical_case())
        part_infl = self.__inflect_forms(participle_forms, part_params)
        obj_adj_params = InflectionParams('adj', sentence_def.object_infl.get_grammatical_case())
        obj_adj_infl = self.__inflect_forms(obj_adjective_forms, obj_adj_params)
        obj_infl = self.__inflect_forms(object_forms, sentence_def.object_infl)

        result = str(predicate_text)
        result = PredicateInflector.__replace_every(result, pred_infl)
        result = PredicateInflector.__replace_every(result, part_infl)
        result = PredicateInflector.__replace_every(result, obj_adj_infl)
        result = PredicateInflector.__replace_every(result, obj_infl)

        return result

    def __inflect_forms(self, forms: list, infl_params: InflectionParams) -> list:
        infl_list = list()
        for f in forms:
            f_inflected = self.inflect_using_params(f.basic, f.params, infl_params)
            infl_list.append((f.inflected, f_inflected))
        return infl_list

    @staticmethod
    def __replace_every(text: str, inflected: list):
        tmp = str(text)
        for inf in inflected:
            tmp = tmp.replace(inf[0], inf[1], 1)
        return tmp
