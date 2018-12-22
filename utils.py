from random import randint
from typing import Any


def random_el(the_list: list) -> Any:
    return the_list[randint(0, len(the_list) - 1)]


def append_if_not_in(element: Any, the_list: list) -> int:
    if element not in the_list:
        the_list.append(element)
        return len(the_list) - 1
    else:
        return the_list.index(element)
