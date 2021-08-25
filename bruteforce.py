#! /usr/bin/env python3
# coding: utf-8


import itertools

from utils import Action, Group, Wrapper


def create_groups(actions, limit_price):
    """ Create all possible groups from an actions list and return the ones whose price is under 500. """
    groups = []
    for size in range(1, len(actions) + 1):
        for group in itertools.combinations(actions, size):
            groups.append(Group(group))
    return [group for group in filter(lambda g: g.price <= limit_price, groups)]


def select_group(actions, limit_price):
    groups = create_groups(actions, limit_price)
    return max(groups, key=lambda g: g.profit)


if __name__ == '__main__':
    Wrapper(select_group).run()