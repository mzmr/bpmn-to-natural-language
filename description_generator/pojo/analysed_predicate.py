from typing import NamedTuple

from description_generator.pojo.word_inflected import WordInflected


class AnalysedPredicate(NamedTuple):
    predicate: WordInflected
    object: WordInflected
    sentence_parts: list
