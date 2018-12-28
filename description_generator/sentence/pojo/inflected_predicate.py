from typing import NamedTuple

from description_generator.sentence.pojo.word_inflected import WordInflected


class InflectedPredicate(NamedTuple):
    predicate: WordInflected
    object: WordInflected
    sentence_parts: list
