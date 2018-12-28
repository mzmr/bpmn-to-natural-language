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
            raise Exception(f'Could not find predicate in sentence: "{predicate_text}".')

        object_forms = extractor.find_objects()
        participle_forms = extractor.find_participles()
        obj_adjective_forms = extractor.find_obj_adjectives()

        # docelowe:
        # wydrukowania kwitów >> bagażowych << -- adj:pl:gen:m1.m2.m3.f.n:pos
        # usunięcie >> zabronionych << przedmiotów -- ppas:pl:gen.loc:m1.m2.m3.f.n:perf:aff

        pred_infl = list()
        for pred in predicate_forms:
            predicate_inflected = self.combine_params_and_inflect(pred.basic, pred.params, sentence_def.predicate_infl)
            pred_infl.append((pred.inflected, predicate_inflected))

        part_infl = list()
        for part in participle_forms:
            participle_inflected = self.combine_params_and_inflect(
                part.basic, part.params, InflectionParams('ppas', sentence_def.object_infl.get_grammatical_case()))
            part_infl.append((part.inflected, participle_inflected))

        obj_adj_infl = list()
        for adj in obj_adjective_forms:
            obj_adjective_inflected = self.combine_params_and_inflect(
                adj.basic, adj.params, InflectionParams('adj', sentence_def.object_infl.get_grammatical_case()))
            obj_adj_infl.append((adj.inflected, obj_adjective_inflected))

        obj_infl = list()
        for obj in object_forms:
            object_inflected = self.combine_params_and_inflect(obj.basic, obj.params, sentence_def.object_infl)
            obj_infl.append((obj.inflected, object_inflected))

        result = str(predicate_text)

        for p in pred_infl:
            result = result.replace(p[0], p[1], 1)

        for p in part_infl:
            result = result.replace(p[0], p[1], 1)

        for a in obj_adj_infl:
            result = result.replace(a[0], a[1], 1)

        for o in obj_infl:
            result = result.replace(o[0], o[1], 1)

        return result
