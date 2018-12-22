import re

from description_generator.consts import genders


class InflectionParams:

    def __init__(self, *args: str):
        self.infl_params = list(args)
        self.__extract_genders(self.infl_params)
        # TODO: tutaj nie powinno się usuwać płci z listy parametrów, a ta metoda powyżej to robi :/

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

        return set(self.infl_params).issubset(their_params)

    def add_param(self, param: str) -> None:
        if param not in self.infl_params:
            self.infl_params.append(param)

    def add_params(self, *params: str) -> None:
        for p in params:
            self.add_param(p)

    @staticmethod
    def inflection_str_to_list(inflection: str) -> list:
        return re.split(r'[:.]', inflection)

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
