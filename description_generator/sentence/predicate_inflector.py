from morfeusz2 import Morfeusz

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
            raise Exception(f'Could not find predicate in sentence: "{predicate_text}".')

        object_forms = extractor.find_objects()

        pred_infl = list()
        for pred in predicate_forms:
            predicate_inflected = self.combine_params_and_inflect(pred.basic, pred.params, sentence_def.predicate_infl)
            pred_infl.append((pred.inflected, predicate_inflected))

        obj_infl = list()
        for obj in object_forms:
            object_inflected = self.combine_params_and_inflect(obj.basic, obj.params, sentence_def.object_infl)
            obj_infl.append((obj.inflected, object_inflected))

        result = str(predicate_text)

        for p in pred_infl:
            result = result.replace(p[0], p[1], 1)

        for o in obj_infl:
            result = result.replace(o[0], o[1], 1)

        return result
