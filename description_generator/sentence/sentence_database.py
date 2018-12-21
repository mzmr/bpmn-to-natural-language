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

    sentences_next = [
        SentenceDef(
            InflectionParams('subst', 'acc'), 2,
            InflectionParams('ger', 'sg', 'nom', 'aff'), 1,
            ('Następnym krokiem jest ', ' przez ', '.'))
    ]

    sentences_and_splitting = [
        SentenceDef(
            InflectionParams(''), 2,
            InflectionParams(''), 1,
            ('W tym momencie następuje podział pracy na X równoległ(e|ych) ścież(ki|ek), wykonywan(e|ych) \
            jednocześnie przez A, B, C i D, opisan(e|ych) kolejno w punktach P, Q, R i S.')
        )
    ]

    sentences_end = [
        'Na tym kończy się powyższy proces.'
    ]
