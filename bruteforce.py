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


def create_groups(actions_list, limit_price):
    """ Create all possible groups from an actions list and return the ones whose price is under 500. """
    groups = []
    for size in range(1, len(actions_list) + 1):
        for actions in itertools.combinations(actions_list, size):
            groups.append(Group(actions))
    return [group for group in filter(lambda g: g.price <= limit_price, groups)]


def main():
    limit_price = 500
    parser = argparse.ArgumentParser(description="Bruteforce dataset to find best actions.")
    parser.add_argument("-i", "--input", help="CSV dataset file to analyse.",
                        required=True, type=argparse.FileType("r"))
    args = parser.parse_args()
    actions = extract_dataset(args.input)
    print(f"*** Extracted {len(actions)} actions from CSV dataset. ***")
    print("*** Generating groups of actions (can take several minutes). ***")
    groups = create_groups(actions, limit_price)
    print(f"*** Generated {len(groups)} groups of actions with a total price under or equal to {limit_price}. ***")
    print("*** Looking for the group with highest profit. ***")
    best_group = max(groups, key=lambda g: g.profit)
    print("*** Best group found ***\n")
    print(best_group)


if __name__ == '__main__':
    main()
