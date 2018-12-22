from description_generator.pojo.sentence_def import SentenceDef
from description_generator.sentence.inflection_params import InflectionParams


class SentenceDatabase:

    __infl_subst_nom = InflectionParams('subst', 'nom')
    __infl_subst_gen = InflectionParams('subst', 'gen')
    __infl_inf_perf = InflectionParams('inf', 'perf')
    __infl_subst_acc = InflectionParams('subst', 'acc')
    __infl_ger_nom_aff = InflectionParams('ger', 'nom', 'aff')
    __infl_ger_gen_aff = InflectionParams('ger', 'gen', 'aff')
    __infl_fin_ter = InflectionParams('fin', 'ter')

    sentences_intro_single = [
        'W tym miejscu poniższy proces ma swój początek.',
        'Opisywany proces rozpoczyna się następującymi zadaniami.'
    ]

    sentences_start = [
        SentenceDef(
            __infl_subst_nom, 1, __infl_inf_perf, 2, __infl_subst_acc,
            ('Na początku ', ' musi ', '.')),
        SentenceDef(
            __infl_subst_acc, 2, __infl_ger_nom_aff, 1, __infl_subst_gen,
            ('Pierwszą czynnością, jaką należy wykonać, jest ', ' przez ', '.')),
        SentenceDef(
            __infl_subst_acc, 2, __infl_ger_gen_aff, 1, __infl_subst_gen,
            ('Poniższy proces rozpoczyna się od ', ' przez ', '.'))
    ]

    sentences_next = [
        SentenceDef(
            __infl_subst_acc, 2, __infl_ger_nom_aff, 1, __infl_subst_gen,
            ('Następnym krokiem jest ', ' przez ', '.')),
        SentenceDef(
            __infl_subst_acc, 2, __infl_ger_nom_aff, 1, __infl_subst_gen,
            ('Kolejną czynnością jest ', ' przez ', '.')),
        SentenceDef(
            __infl_subst_acc, 2, __infl_ger_nom_aff, 1, __infl_subst_gen,
            ('Kolejny krok, to ', ' przez ', '.')),
        SentenceDef(
            __infl_subst_nom, 1, __infl_fin_ter, 2, __infl_subst_acc,
            ('Następnie ', ' ', '.')),
        SentenceDef(
            __infl_subst_nom, 1, __infl_fin_ter, 2, __infl_subst_acc,
            ('Później ', ' ', '.')),
        SentenceDef(
            __infl_subst_nom, 1, __infl_fin_ter, 2, __infl_subst_acc,
            ('Potem ', ' ', '.')),
        SentenceDef(
            __infl_subst_nom, 1, __infl_fin_ter, 2, __infl_subst_acc,
            ('Następnie ', ' ', '.')),
    ]

    # TODO: wykorzystać zdania bez podmiotu, gdy dany podmiot wykonuje więcej niż jedno zadanie pod rząd
    sentences_next_no_subject = [
        SentenceDef(
            None, None,
            InflectionParams(), 1, __infl_subst_gen,
            ('Na tym etapie następuje ', '.')),
        SentenceDef(
            None, None,
            InflectionParams(), 1,  __infl_subst_acc,
            ('Na tym etapie należy ', '.')),
    ]

    sentences_and_splitting = [
        SentenceDef(
            InflectionParams('subst', 'acc'), 1,
            None, None, None,
            ('W tym momencie następuje podział pracy na równoległe ścieżki, wykonywane jednocześnie przez ',
             ', opisane odpowiednio w punktach ', '.'))
    ]

    sentences_and_joining = [
        SentenceDef(
            InflectionParams('subst', 'nom'), 1,
            None, None, None,
            ('Teraz należy poczekać, aż ', ' zakończą swoje zadania, opisane na końcu punktów ', '.')
        )
    ]

    sentences_end = [
        'Na tym kończy się powyższy proces.'
    ]
