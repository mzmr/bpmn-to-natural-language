from typing import NamedTuple

from pojo.word_inflected import WordInflected


class IsolatedSubject(NamedTuple):
    subject: WordInflected
    adjective: WordInflected
    genitive: WordInflected
