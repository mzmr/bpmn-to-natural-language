from random import randint


def random_el(the_list: list):
    return the_list[randint(0, len(the_list) - 1)]