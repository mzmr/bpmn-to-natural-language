import re


class InflectionParams:

    def __init__(self, *args: str):
        self.infl_params = list(args)
        self.__genders = {
            'm': ['m1', 'm2', 'm3'],
            'f': ['f1', 'f2', 'f3'],
            'n': ['n1', 'n2', 'n3']
        }
        self.__extract_genders(self.infl_params)

    def matches(self, inflection_string: str):
        their_params = re.split(r'[:.]', inflection_string)
        my_genders = self.__extract_genders(self.infl_params)

        if my_genders and not any(g in their_params for g in my_genders):
            return False

        return set(self.infl_params).issubset(their_params)

    def __extract_genders(self, params: list):
        genders = list()

        for key, values in self.__genders.items():
            if key in params:
                genders.extend(values)
                params.remove(key)

            for val in values:
                if val in params:
                    genders.append(val)
                    params.remove(val)

        return genders


#     STARA WERSJA TEJ KLASY:
#
#     def __init__(self, parts_of_speech: list, singular_plural: list, case: str, gender: list):
#         self.parts_of_speech = parts_of_speech
#         self.sg_pl = singular_plural
#         self.case = case
#         self.gender = gender
#         self.masculines = 'm', 'm1', 'm2', 'm3'
#         self.females = 'f', 'f1', 'f2', 'f3'
#         self.neuters = 'n', 'n1', 'n2', 'n3'
#
#     def matches(self, inflection_string: str):
#         their_params = re.split(r'[:.]', inflection_string)
#         self.__general_to_detail(their_params)
#         my_params = [self.parts_of_speech, self.sg_pl, self.case, self.gender]
#         self.__general_to_detail(my_params)
#         return set(my_params).issubset(their_params)
#
#     def __create_my_params_list(self):
#         params = []
#         params.extend(self.parts_of_speech)
#         params.extend(self.sg_pl)
#         params.append(self.case)
#         params.extend(self.gender)
#         return params
#
#     def __general_to_detail(self, params: list):
#         if 'f' in params:
#             params.extend(self.females[1:])
#         if 'm' in params:
#             params.extend(self.masculines[1:])
#         if 'n' in params:
#             params.extend(self.neuters[1:])
