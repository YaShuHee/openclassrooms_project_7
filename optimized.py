#! /usr/bin/env python3
# coding: utf-8


from utils import Action, Group, Wrapper


def select_group(actions, limit_price):
    """ Sort the actions by price_by_profit. Makes a group whose price is under the limit price, from the best actions.
    """
    price, c, last_kept = 0, 0, 0
    to_keep = []
    length = len(actions)

    average_price_by_profit = Group(actions).price_by_profit

    actions = sorted(actions, key=lambda action: action.price)
    actions = sorted(actions, key=lambda action: action.profit, reverse=True)
    actions = sorted(actions, key=lambda action: action.price_by_profit)

    while c < length:
        simulation = price + actions[c].price
        if simulation < limit_price and actions[c].price_by_profit < average_price_by_profit * 1.5:
            price = simulation
            to_keep.append(actions[c])
            last_kept = c
        c += 1
    c = last_kept + 1

    while c < length:
        active_group = Group(to_keep)
        tmp_group = Group(to_keep[:-1] + [actions[c]])
        if tmp_group.price < limit_price and actions[c].price_by_profit < average_price_by_profit * 1.5\
                and tmp_group.price_by_profit > active_group.price_by_profit:
            to_keep[-1] = actions[c]
        c += 1

    return Group(to_keep)


if __name__ == '__main__':
    Wrapper(select_group).run()
