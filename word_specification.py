# NA RAZIE ZAUTOMATYZOWANIE TEGO NIE JEST DO ZROBIENIA, BO NIE ZNAM PEŁNYCH ZASAD TWORZENIA TYPÓW (LEMATÓW CZY JAKOŚ TAK)


class WordSpec:

    def __init__(self, form: list, number: str, case: list, conjugation: list = None, tense: list = None, aff_neg: str = None):
        self.form = form
        self.number = number
        self.case = case
        self.conjugation = conjugation
        self.tense = tense
        self.aff_neg = aff_neg

    @classmethod
    def create_from_typestring(cls, typestr: str):
        params = typestr.split(':')

        if len(params) == 2:
            pass

        if len(params) < 4:
            raise Exception(f'Too little parameters ({len(params)}) in type "{typestr}".')

        dot = '.'
        form = params[0].split(dot)
        number = params[1]  # number should be the string, not the list
        case = params[2].split(dot)
        conjugation = params[3].split(dot)
        tense = None
        aff_neg = None

        if len(params) == 6:
            tense = params[4].split(dot)
            aff_neg = params[5]  # aff_neg should be the string, not the list

        return cls(form, number, case, conjugation, tense, aff_neg)

    def generate_typestrings(self):
        dot = '.'
        form_str = dot.join(self.form)
        number_str = self.number
        case_str = dot.join(self.case)
        conjugation_str = dot.join(self.conjugation)

        if self.tense is not None and self.aff_neg is not None:
            tense_str = dot.join(self.tense)
            aff_neg_str = self.aff_neg
            return f'{form_str}:{number_str}:{case_str}:{conjugation_str}:{tense_str}:{aff_neg_str}'
        else:
            return f'{form_str}:{number_str}:{case_str}:{conjugation_str}'

    def matches(self, word_spec: 'WordSpec'):
        if WordSpec.__params_different(self.form, word_spec.form):
            return False

        if self.number != word_spec.number:
            return False

        if WordSpec.__params_different(self.case, word_spec.case):
            return False

        if WordSpec.__params_different(self.conjugation, word_spec.conjugation):
            return False

        if self.tense is not None and word_spec.tense is not None:
            if WordSpec.__params_different(self.tense, word_spec.tense):
                return False

        if self.aff_neg is not None and word_spec.aff_neg is not None:
            if self.aff_neg != word_spec.aff_neg:
                return False

    @staticmethod
    def __params_different(param1: list, param2: list):
        return len(set(param1).intersection(param2)) == 0
