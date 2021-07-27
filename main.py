#! /usr/bin/env python3
# coding: utf-8


import argparse
import csv
import itertools


class Action:
    """ An object to access to actions properties easily. """
    def __init__(self, name: str, price: str, profit: str):
        self.name = name
        self.price = float(price)
        if profit.endswith("%"):
            profit = profit[:-1]
        self.profit = float(profit)

    def __repr__(self):
        return f"<{self.name}\t{self.price}€\t{self.profit}%>"


def calculate_group_price(group):
    """ Returns the price of an actions group. """
    price = 0
    for action in group:
        price += action.price
    return price


def extract_dataset(csv_file) -> list:
    """ Extract the dataset from a CSV file. """
    with csv_file:
        reader = csv.DictReader(csv_file)
        return [Action(**action_row) for action_row in reader]


def create_groups(actions_list, limit_price):
    """ Create all possible groups from an actions list and return the ones whose price is under 500. """
    groups = []
    for size in range(1, len(actions_list) + 1):
        for group in itertools.combinations(actions_list, size):
            groups.append(group)
    return [group for group in filter(lambda g: calculate_group_price(g) <= limit_price, groups)]


def calculate_group_profit(group):
    """ Calculate an actions group profit. """
    group_profit = 0
    for action in group:
        group_profit += action.price * action.profit/100
    return [action.name for action in group], round(group_profit, 2)


def archive_results(results, csv_file_name):
    try:
        with open(csv_file_name, "w", newline="") as csv_file:
            writer = csv.writer(csv_file, delimiter=",")
            writer.writerow(["actions", "profit"])
            writer.writerows(results)
    except PermissionError:
        csv_file_name = csv_file_name[:-4] + "_" + ".csv"
        print("/!\ The file is already opened and can't be modified.")
        print(f"/!\ A file named '{csv_file_name}' will be created instead")
        archive_results(results, csv_file_name)
    return csv_file_name


def main():
    limit_price = 500
    parser = argparse.ArgumentParser(description="Bruteforce dataset to find best actions.")
    parser.add_argument("-d", "--dataset-file", help="CSV dataset file to analyse.",
                        required=True, type=argparse.FileType("r"))
    parser.add_argument("-r", "--results-file", help="CSV file name to create.")
    args = parser.parse_args()
    actions = extract_dataset(args.dataset_file)
    print(f"*** Extracted {len(actions)} actions from CSV dataset. ***")
    print("*** Generating groups of actions (can take several minutes). ***")
    groups = create_groups(actions, limit_price)
    print(f"*** Generated {len(groups)} groups of actions with a total price under or equal to {limit_price}. ***")
    results = [calculate_group_profit(group) for group in groups]
    print("*** Generating results CSV. ***")
    file_name = archive_results(results, args.results_file)
    print(f"*** Successfully created CSV file '{file_name}'. ***")


if __name__ == '__main__':
    main()
