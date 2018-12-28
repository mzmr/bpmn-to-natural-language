from morfeusz2 import Morfeusz

from description_generator.sentence.consts import genders
from description_generator.sentence.pojo.word_inflected import WordInflected
from description_generator.sentence.inflection_params import InflectionParams


class PartOfSpeechExtractor:

    def __init__(self, text: str, morfeusz: Morfeusz):
        self.analysis = morfeusz.analyse(text)

    def find_subjects(self) -> list:
        # maybe it should be nom OR ger, not only nom?
        return self.__find_forms(InflectionParams('subst', 'nom'))

    def find_adjectives(self, related_subject_inflection: str) -> list:
        params = InflectionParams.inflection_str_to_list(related_subject_inflection)

        gender = self.find_gender(params)
        sg_or_pl = self.find_sg_or_pl(params)

        if gender:
            return self.__find_forms(InflectionParams('adj', 'nom', gender, sg_or_pl))
        else:
            return self.__find_forms(InflectionParams('adj', 'nom', sg_or_pl))

    def find_genitives(self) -> list:
        return self.__find_forms(InflectionParams('subst', 'gen'))

    def find_predicates(self) -> list:
        return self.__find_forms(InflectionParams('impt'))

    def find_objects(self) -> list:
        return self.__find_forms(InflectionParams('subst', 'acc'))

    def find_participles(self) -> list:
        # szukane:
        # usuń >> zabronione << -- przemioty -- ppas:pl:nom.acc.voc:m2.m3.f.n:perf:aff
        return self.__find_forms(InflectionParams('ppas', 'acc'))

    def find_obj_adjectives(self) -> list:
        # szukane:
        # wydrukuj kwity >> bagażowe << -- adj:pl:acc:m2.m3.f.n:pos
        return self.__find_forms(InflectionParams('adj', 'acc'))

    @staticmethod
    def find_gender(params: list) -> str:
        for group_name, subgroup_names in genders.items():
            if group_name in params:
                return group_name

            for subgroup_name in subgroup_names:
                if subgroup_name in params:
                    return subgroup_name

        return ''

    @staticmethod
    def find_sg_or_pl(params: list) -> str:
        for p in params:
            if p == 'sg':
                return 'sg'

            if p == 'pl':
                return 'pl'

        raise Exception(f'Couldn\'t find gender in type "{params}"')

    def __find_forms(self, params: InflectionParams) -> list:
        forms_found = list()
        nums_to_remove = list()
        prep_appeared = False

        for an in self.analysis:
            word_type = PartOfSpeechExtractor.__get_word_type(an)

            if 'prep' in word_type:
                prep_appeared = True

            if prep_appeared and 'subst' in params.infl_params:
                break

            if PartOfSpeechExtractor.__get_word_number(an) in nums_to_remove:
                continue

            if params.matches(word_type):
                basic = PartOfSpeechExtractor.__get_basic_word_form(an)
                inflected = PartOfSpeechExtractor.__get_inflected_word_form(an)
                forms_found.append(WordInflected(basic, inflected, word_type))
                word_number = PartOfSpeechExtractor.__get_word_number(an)
                nums_to_remove.append(word_number)

        self.__remove_word_with_num(nums_to_remove)
        return forms_found

    @staticmethod
    def __get_word_type(an: tuple) -> str:
        return an[2][2]

    @staticmethod
    def __get_basic_word_form(an: tuple) -> str:
        return an[2][1]

    @staticmethod
    def __get_inflected_word_form(an: tuple) -> str:
        return an[2][0]

    @staticmethod
    def __get_word_number(an: tuple) -> int:
        return an[0]

    def __remove_word_with_num(self, nums_to_remove: list) -> None:
        self.analysis = [an for an in self.analysis if self.__get_word_number(an) not in nums_to_remove]
