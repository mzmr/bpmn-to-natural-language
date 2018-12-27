from typing import NamedTuple

from description_generator.sentence.pojo.word_inflected import WordInflected


class ExtractedSubject(NamedTuple):
    subject: WordInflected
    adjective: WordInflected
    genitive: WordInflected
