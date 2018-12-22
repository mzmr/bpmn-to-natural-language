from collections import namedtuple

from description_generator.sentence.inflection_params import InflectionParams

SentenceDef = namedtuple('SentenceDef', 'subject_infl subject_order predicate_infl predicate_order text_list')


class SentenceDatabase:

    sentences_intro_single = [
        'W tym miejscu poniższy proces ma swój początek.',
        'Opisywany proces rozpoczyna się następującymi zadaniami.'
    ]

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
            InflectionParams('subst', 'acc'), 1,
            None, None,
            ('W tym momencie następuje podział pracy na równoległe ścieżki, wykonywane jednocześnie przez ',
             ', opisane odpowiednio w punktach ', '.'))
    ]

    sentences_and_joining = [
        SentenceDef(
            InflectionParams('subst', 'nom'), 1,
            None, None,
            ('Teraz należy poczekać, aż ', ' zakończą swoje zadania, opisane na końcu punktów ', '.')
        )
    ]

    sentences_end = [
        'Na tym kończy się powyższy proces.'
    ]
