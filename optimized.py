#! /usr/bin/env python3
# coding: utf-8


import argparse
import csv
import itertools

from utils import Action, Group


def extract_dataset(csv_file) -> list:
    """ Extract the dataset from a CSV file. """
    with csv_file:
        reader = csv.DictReader(csv_file)
        return [Action(**action_row) for action_row in reader]


def create_group(actions, limit_price):
    """ Sort the actions by profit. Makes a group whose price is under the limit price, from the best actions."""
    price, c = 0, 0
    to_keep = []
    length = len(actions)
    actions = sorted(actions, key=lambda action: action.price)
    actions = sorted(actions, key=lambda action: action.profit, reverse=True)
    while c < length:
        simulation = price + actions[c].price
        if simulation < 500:
            price = simulation
            to_keep.append(actions[c])
        c += 1
    return Group(to_keep)


def main():
    limit_price = 500
    parser = argparse.ArgumentParser(description="Bruteforce dataset to find best actions.")
    parser.add_argument("-i", "--input", help="CSV dataset file to analyse.",
                        required=True, type=argparse.FileType("r"))
    args = parser.parse_args()
    actions = extract_dataset(args.input)
    old_len = len(actions)
    print(f"*** Extracted {old_len} actions from CSV dataset. ***")
    print("*** Sorting actions and removing worst. ***")
    best_group = create_group(actions, limit_price)
    new_len = len(actions)
    print(f"*** Sorted and kept {new_len} actions (removed {old_len - new_len} of {old_len}). ***")
    print("*** Best group found ***\n")
    print(best_group)


if __name__ == '__main__':
    main()
