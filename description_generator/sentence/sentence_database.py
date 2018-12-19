from collections import namedtuple

from description_generator.sentence.inflection_params import InflectionParams

SentenceDef = namedtuple('SentenceDef', 'subject_infl subject_order predicate_infl predicate_order text_list')


class SentenceDatabase:
    sentences_start = [
        SentenceDef(
            InflectionParams('subst', 'sg', 'nom'), 1,
            InflectionParams('inf', 'perf'), 2,
            ('Na początku ', ' musi ', '.')),
        SentenceDef(
            InflectionParams('subst', 'acc'), 2,
            InflectionParams('ger', 'sg', 'nom', 'aff'), 1,
            ('Pierwszą czynnością, jaką należy wykonać, jest ', ' przez ', '.')),
        SentenceDef(
            InflectionParams('subst', 'acc'), 2,
            InflectionParams('ger', 'sg', 'gen', 'aff'), 1,
            ('Poniższy proces rozpoczyna się od ', ' przez ', '.'))
    ]
