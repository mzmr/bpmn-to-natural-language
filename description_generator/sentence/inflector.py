from morfeusz2 import Morfeusz

from description_generator.sentence.inflection_params import InflectionParams
from description_generator.sentence.part_of_speech_extractor import PartOfSpeechExtractor


class Inflector:

    def __init__(self, morfeusz: Morfeusz):
        self.morf = morfeusz

    def combine_params_and_inflect(self, basic_word: str, word_infl_par: str,
                                     basic_infl_par: InflectionParams) -> str:
        infl_params = Inflector.__create_target_infl_params(word_infl_par, basic_infl_par)
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
