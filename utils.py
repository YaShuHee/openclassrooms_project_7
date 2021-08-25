#! /usr/bin/env python3
# coding: utf-8


from abc import ABC
import argparse
import time
import csv

import pandas


# Displays floats rounded to two decimal places or ints.
pandas.options.display.float_format = lambda n: str(int(n)) if int(n) == n else "{:.2f}".format(n)


class Serializable(ABC):
    """ An abstract class that can be serialized. """
    @property
    def serialized(self):
        to_serialize = ["name", "price (€)", "profit (€)", "price_by_profit", "index_number"]
        return {
            key.capitalize().replace("_", " "): object.__getattribute__(self, key.replace(" (€)", ""))
            for key in to_serialize
        }


class Action(Serializable):
    """ A class to access to actions properties easily. """
    def __init__(self, name: str, price: str, profit: str):
        self.price = float(price)
        self.profit_percentage = float(profit)
        # We mark invalid actions (negative price or profit) so the main algorithm don't have to deal with it later.
        if self.price <= 0 or self.profit_percentage <= 0:
            self.valid = False
            self.name = None
            self.price = None
            self.profit = None
            self.profit_percentage = None
            self.price_by_profit = None
            self.index_number = None
        else:
            self.valid = True
            self.name = name
            self.profit = self.price * self.profit_percentage / 100
            self.price_by_profit = round(self.price / self.profit, 5)
            self.index_number = round((500 / self.price)**(1/self.price_by_profit), 4)

    def __str__(self):
        return f"{self.name}({self.price}€) => +{self.profit}€"


class Group(Serializable):
    """ A class to access a resume of several actions, their total cost and total profit. """
    def __init__(self, actions: list[Action]):
        self.actions = actions
        self.price = self._sum_attribute("price")
        self.profit = self._sum_attribute("profit")
        self.price_by_profit = self.price / self.profit
        self.index_number = round((500/self.price)**(1/self.price_by_profit), 4)

    def __str__(self):
        data = [action.serialized for action in sorted(self.actions, key=lambda a: a.index_number, reverse=True)]
        self.name = "TOTAL"
        data.append(self.serialized)
        df = pandas.DataFrame(data)
        return df.to_string(index=False)

    def _sum_attribute(self, key):
        """ Makes the sum of an attribute from all actions
        (example: sum the prices of this group actions, to know this group price). """
        sum_ = 0
        for action in self.actions:
            sum_ += object.__getattribute__(action, key)
        return sum_


class DataSet:
    """ A class that will extract data from csv file and clean it up, so the main algorithm don't have to deal with
    irrelevant data. """
    def __init__(self, csv_file):
        self._file = csv_file
        self._data_set = []

    def _extract_dataset(self):
        """ Extracts the dataset from a CSV file. """
        with self._file:
            reader = csv.DictReader(self._file)
            self._data_set = [Action(**action_row) for action_row in reader]

    def _clean_dataset(self):
        """ Removes the actions previously marked as invalid. """
        self._data_set = [action for action in filter(lambda a: a.valid is True, self._data_set)]

    def get_actions(self):
        """ Extracts, cleans up and returns the actions."""
        self._extract_dataset()
        self._clean_dataset()
        return self._data_set


class Wrapper:
    """ This class exists so bruteforce.py and optimized.py can keep only very basic stuff.
    Only their differences are kept, so it is more readable. """
    def __init__(self, algorithm):
        """ Takes a callable as an entry. The callable will be the main algorithm to select actions. """
        self.function = algorithm
        self.limit_price = 500
        self.verbose = True
        self.csv_file = ""
        self.actions = []
        self.selected_group = None

    def _parse(self):
        """ Builds the parser. """
        parser = argparse.ArgumentParser(description="Bruteforce dataset to find best actions.")
        parser.add_argument("-i", "--input", help="CSV dataset file to analyse.",
                            required=True, type=argparse.FileType("r"))
        parser.add_argument("-v", '--verbose', help="Verbose mode active when used.", action="store_true")
        parser.add_argument("-t", '--time', help="Displays algorithm duration when active.", action="store_true")
        args = parser.parse_args()
        self.csv_file = args.input
        self.verbose = args.verbose
        self.time = args.time

    def _get_actions(self):
        """ Uses the DataSet class to extract and clean up all the actions before any data treatment. """
        data_set = DataSet(self.csv_file)
        self.actions = data_set.get_actions()

    def run(self):
        """ Main method in which the parsing, actions extractions and algorithm to test are called. """
        self._parse()
        if self.verbose:
            print("Extracting actions list from input file.")
        self._get_actions()
        if self.verbose:
            print(f"Extracted {len(self.actions)} actions.")
        print("Selecting a group.")
        if self.time:
            start_time = time.time()
        self.selected_group = self.function(self.actions, self.limit_price)
        if self.time:
            end_time = time.time()
        print(f"Selected group : \n\n{self.selected_group}")
        if self.time:
            print(f"\nExecution time: {end_time - start_time} seconds.\n")

