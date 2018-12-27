from typing import NamedTuple

from description_generator.sentence.inflection_params import InflectionParams


class SentenceDef(NamedTuple):
    subject_infl: InflectionParams
    subject_order: int
    predicate_infl: InflectionParams
    predicate_order: int
    object_infl: InflectionParams
    text_list: tuple
