from random import randint


def random_el(the_list: list):
    return the_list[randint(0, len(the_list) - 1)]


def append_if_not_in(element, the_list: list):
    if element not in the_list:
        the_list.append(element)
        return len(the_list) - 1
    else:
        return the_list.index(element)
