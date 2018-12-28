import re

from description_generator.sentence.consts import genders


class InflectionParams:

    def __init__(self, *args: str):
        self.infl_params = list(args)
        # self.__extract_genders(self.infl_params)

    def clone(self):
        new_obj = InflectionParams()
        new_obj.infl_params = list(self.infl_params)
        return new_obj

    def matches(self, inflection: str) -> bool:
        their_params = InflectionParams.inflection_str_to_list(inflection)
        my_genders = InflectionParams.__extract_genders(self.infl_params)
        their_genders = InflectionParams.__extract_genders(their_params)

        if my_genders and their_genders and \
                not any(g in their_genders for g in my_genders):
            return False

        matches = set(self.infl_params).issubset(their_params)
        self.infl_params.extend(my_genders)
        their_params.extend(their_genders)
        return matches

    def add_param(self, param: str) -> None:
        if (param in ['sg', 'pl']) and 'inf' in self.infl_params:
            return

        if param not in self.infl_params:
            self.infl_params.append(param)

    def add_params(self, *params: str) -> None:
        for p in params:
            self.add_param(p)

    @staticmethod
    def inflection_str_to_list(inflection: str) -> list:
        return re.split(r'[:.]', inflection)

    def get_grammatical_case(self):
        cases = ['nom', 'gen', 'dat', 'acc', 'inst', 'loc', 'voc']
        for c in cases:
            if c in self.infl_params:
                return c

    @staticmethod
    def __extract_genders(params: list) -> list:
        genders_extracted = list()

        for key, values in genders.items():
            if key in params:
                genders_extracted.extend(values)
                params.remove(key)

            for val in values:
                if val in params:
                    genders_extracted.append(val)
                    params.remove(val)

        return genders_extracted
