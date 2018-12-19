from collections import namedtuple

from morfeusz2 import Morfeusz

from sentence.inflection_params import InflectionParams

WordFound = namedtuple('AnalysedWord', 'basic inflected')


class AnalyserAdapter:

    def __init__(self, text: str, morfeusz: Morfeusz):
        self.analysis = morfeusz.analyse(text)

    def find_subjects(self):
        # maybe it should be nom OR ger, not only nom?
        return self.__find_forms(InflectionParams('subst', 'nom'))

    def find_adjectives(self):
        return self.__find_forms(InflectionParams('adj', 'nom'))

    def find_genitives(self):
        return self.__find_forms(InflectionParams('subst', 'gen'))

    def find_predicates(self):
        return self.__find_forms(InflectionParams('impt'))

    def __find_forms(self, params: InflectionParams):
        forms_found = list()
        nums_to_remove = list()

        for an in self.analysis:
            word_type = AnalyserAdapter.__get_word_type(an)

            if params.matches(word_type):
                basic = AnalyserAdapter.__get_basic_word_form(an)
                inflected = AnalyserAdapter.__get_inflected_word_form(an)
                forms_found.append(WordFound(basic, inflected))
                word_number = AnalyserAdapter.__get_word_number(an)
                nums_to_remove.append(word_number)

        self.__remove_word_with_num(nums_to_remove)
        return forms_found

    @staticmethod
    def __get_word_type(an: tuple):
        return an[2][2]

    @staticmethod
    def __get_basic_word_form(an: tuple):
        return an[2][1]

    @staticmethod
    def __get_inflected_word_form(an: tuple):
        return an[2][0]

    @staticmethod
    def __get_word_number(an):
        return an[0]

    def __remove_word_with_num(self, nums_to_remove: list):
        self.analysis = [an for an in self.analysis if self.__get_word_number(an) not in nums_to_remove]
