from description_generator.sentence.pojo.sentence_def import SentenceDef
from description_generator.sentence.inflection_params import InflectionParams


class SentenceDatabase:

    __infl_subst_nom = InflectionParams('subst', 'nom')
    __infl_subst_gen = InflectionParams('subst', 'gen')
    __infl_inf_perf = InflectionParams('inf', 'perf')
    __infl_subst_acc = InflectionParams('subst', 'acc')
    __infl_ger_nom_aff = InflectionParams('ger', 'nom', 'aff')
    __infl_ger_gen_aff = InflectionParams('ger', 'gen', 'aff')
    __infl_ger_acc_perf_aff = InflectionParams('ger', 'acc', 'perf', 'aff')
    __infl_ger_inst = InflectionParams('ger', 'inst')
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

    sentences_start_no_subject = [
        SentenceDef(
            None, None, __infl_inf_perf, 1, __infl_subst_acc,
            ('Na początku trzeba ', '.')),
        SentenceDef(
            None, None, __infl_ger_nom_aff, 1, __infl_subst_gen,
            ('Pierwszą czynnością, jaką należy wykonać, jest ', '.')),
        SentenceDef(
            None, None, __infl_ger_gen_aff, 1, __infl_subst_gen,
            ('Poniższy proces rozpoczyna się od ', '.'))
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
            __infl_subst_gen, 1, __infl_inf_perf, 2, __infl_subst_acc,
            ('Kolejne zadanie należy do ', '. Musi on ', '.')),
        SentenceDef(
            __infl_subst_nom, 1, __infl_inf_perf, 2, __infl_subst_acc,
            ('Następnie ', ' musi ', '.')),
        SentenceDef(
            __infl_subst_nom, 1, __infl_inf_perf, 2, __infl_subst_acc,
            ('Później ', ' musi ', '.')),
        SentenceDef(
            __infl_subst_nom, 1, __infl_inf_perf, 2, __infl_subst_acc,
            ('Potem ', ' musi ', '.')),
    ]

    sentences_next_default_subject = [
        SentenceDef(
            None, None,
            __infl_ger_nom_aff, 1, __infl_subst_gen,
            ('Na tym etapie następuje ', '.')),
        SentenceDef(
            None, None,
            __infl_inf_perf, 1, __infl_subst_acc,
            ('Na tym etapie należy ', '.')),
        SentenceDef(
            None, None,
            __infl_fin_ter, 1, __infl_subst_acc,
            ('Następnie ', '.')),
        SentenceDef(
            None, None,
            __infl_fin_ter, 1, __infl_subst_acc,
            ('Później ', '.')),
        SentenceDef(
            None, None,
            __infl_fin_ter, 1, __infl_subst_acc,
            ('Potem ', '.')),
        SentenceDef(
            None, None,
            __infl_inf_perf, 1, __infl_subst_acc,
            ('Następnie musi on ', '.')),
        SentenceDef(
            None, None,
            __infl_inf_perf, 1, __infl_subst_acc,
            ('Później musi on ', '.')),
        SentenceDef(
            None, None,
            __infl_inf_perf, 1, __infl_subst_acc,
            ('Potem musi on ', '.')),
        SentenceDef(
            None, None,
            __infl_ger_nom_aff, 1, __infl_subst_gen,
            ('Kolejnym jego zadaniem jest ', '.')),
    ]

    sentences_next_no_subject = [
        SentenceDef(
            None, None,
            __infl_ger_nom_aff, 1, __infl_subst_gen,
            ('Na tym etapie następuje ', '.')),
        SentenceDef(
            None, None,
            __infl_inf_perf, 1, __infl_subst_acc,
            ('Na tym etapie należy ', '.')),
        SentenceDef(
            None, None,
            __infl_inf_perf, 1, __infl_subst_acc,
            ('Następnie trzeba ', '.')),
        SentenceDef(
            None, None,
            __infl_inf_perf, 1, __infl_subst_acc,
            ('Później należy ', '.')),
        SentenceDef(
            None, None,
            __infl_ger_nom_aff, 1, __infl_subst_gen,
            ('Potem następuje ', '.')),
        SentenceDef(
            None, None,
            __infl_ger_nom_aff, 1, __infl_subst_gen,
            ('Kolejnym zadaniem jest ', '.')),
    ]

    sentences_and_splitting = [
        SentenceDef(
            InflectionParams('subst', 'acc'), 1,
            None, None, None,
            ('W tym momencie następuje podział pracy na równoległe ścieżki, wykonywane jednocześnie przez ',
             ', opisane odpowiednio w punktach ', '.'))
    ]

    sentences_and_splitting_no_subject = [
            ('W tym momencie następuje podział pracy na równoległe ścieżki opisane w punktach ', '.')
    ]

    sentences_and_joining = [
        SentenceDef(
            InflectionParams('subst', 'nom'), 1,
            None, None, None,
            ('Teraz należy poczekać, aż ', ' zakończą swoje zadania, opisane na końcu punktów ', '.'))
    ]

    sentences_and_joining_no_subject = [
            ('By kontynuować, należy poczekać, aż punkty ', ' zostaną zakończone.')
    ]

    sentences_xor_splitting = [
        (  # np: Kawa czy herbata? Jeśli X
         ', to należy przejść do punktu ', '.', 'Można wybrać tylko jedną z odpowiedzi.')
    ]

    sentences_xor_joining = [
        'Po zakończeniu wcześniej wybranej ścieżki, proces jest tu kontynuowany.'
    ]

    sentences_or_splitting = [
        (', to należy przejść do punktu ', '.', 'Można wybrać jedną lub więcej odpowiedzi.')
    ]

    sentences_or_joining = [
        'Po zakończeniu wcześniej wybranych ścieżek, proces jest kontynuowany w tym punkcie.'
    ]

    sentences_end = [
        'Na tym kończy się powyższy proces.'
    ]

    sentences_group_end = [
        ('Po zakończeniu tego punktu należy przejść do punktu ', '.'),
        ('Na tym się kończy ten punkt. Dalsze instrukcje znajdują się w punkcie ', '.'),
        ('Następnie należy przejść do punktu ', '.'),
        ('Kolejne zadania opisane są w punkcie ', '.')
    ]

    sentences_group_start = [
        SentenceDef(
            __infl_subst_nom, 1, __infl_ger_acc_perf_aff, 2, __infl_subst_gen,
            ('W tym punkcie ', ' odpowiada za ', '.')),
        SentenceDef(
            __infl_subst_nom, 1, __infl_ger_inst, 2, __infl_subst_gen,
            ('W tym punkcie ', ' zajmuje się ', '.')),
        SentenceDef(
            __infl_subst_acc, 2, __infl_ger_gen_aff, 1, __infl_subst_gen,
            ('Ten punkt zaczyna się od ', ' przez ', '.')),
    ]

    sentences_group_start_no_subject = [
        SentenceDef(
            None, None, __infl_ger_nom_aff, 1, __infl_subst_gen,
            ('Pierwszym zadaniem w tym punkcie jest ', '.')),
        SentenceDef(
            None, None, __infl_inf_perf, 1, __infl_subst_acc,
            ('W tym punkcie należy ', '.')),
        SentenceDef(
            None, None, __infl_ger_gen_aff, 1, __infl_subst_gen,
            ('Ten punkt zaczyna się od ', '.')),
    ]
