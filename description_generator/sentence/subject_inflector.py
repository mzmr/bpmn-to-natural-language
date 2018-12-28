from morfeusz2 import Morfeusz

from description_generator.sentence.inflector import Inflector
from description_generator.sentence.part_of_speech_extractor import PartOfSpeechExtractor
from description_generator.sentence.pojo.sentence_def import SentenceDef


class SubjectInflector(Inflector):

    def __init__(self, morfeusz: Morfeusz):
        Inflector.__init__(self, morfeusz)

    def inflect(self, subject_text: str, sentence_def: SentenceDef) -> str:
        extractor = PartOfSpeechExtractor(subject_text.lower(), self.morf)

        subject_forms = extractor.find_subjects()
        if subject_forms:
            sub = subject_forms[0]
        else:
            raise Exception(f'Could not find subject in "{subject_text}".')

        adj = None
        adjective_forms = extractor.find_adjectives(sub.params)
        if adjective_forms:
            adj = adjective_forms[0]

        gen = None
        genitive_forms = extractor.find_genitives()
        if genitive_forms:
            gen = genitive_forms[0]

        sub_infl = self.combine_params_and_inflect(sub.basic, sub.params, sentence_def.subject_infl)

        if adj is None:
            adj_infl = ''
        else:
            adj_infl = f' {adj.inflected}'

        if gen is None:
            gen_infl = ''
        else:
            gen_infl = f' {gen.inflected}'

        return f'{sub_infl}{adj_infl}{gen_infl}'
