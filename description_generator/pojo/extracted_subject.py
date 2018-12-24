from typing import NamedTuple

from description_generator.pojo.word_inflected import WordInflected


class ExtractedSubject(NamedTuple):
    subject: WordInflected
    adjective: WordInflected
    genitive: WordInflected
