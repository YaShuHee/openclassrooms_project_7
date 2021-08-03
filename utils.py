from abc import ABC

import pandas

# Displays int XOR floats rounded to two decimal places.
pandas.options.display.float_format = lambda n: str(int(n)) if int(n) == n else "{:.2f}".format(n)


class Serializable(ABC):
    """ An abstract class that can be serialized. """
    @property
    def serialized(self):
        to_serialize = ["name", "price (€)", "profit (€)", "price_by_profit"]
        return {
            key.capitalize().replace("_", " "): object.__getattribute__(self, key.replace(" (€)", ""))
            for key in to_serialize
        }


class Action(Serializable):
    """ An object to access to actions properties easily. """
    def __init__(self, name: str, price: str, profit: str):
        self.name = name
        self.price = float(price)
        self.profit_percentage = float(profit)
        self.profit = self.price * self.profit_percentage / 100
        self.price_by_profit = round(self.price / self.profit, 5)

    def __str__(self):
        return f"{self.name}({self.price}€) => +{self.profit}€"


class Group(Serializable):
    """ An object to access a resume of several actions, their total cost and total profit. """
    def __init__(self, actions: list[Action]):
        self.actions = actions
        self.price = self.calculate_price()
        self.profit = self.calculate_profit()
        self.price_by_profit = self.calculate_price_by_profit()

    def __str__(self):
        data = [action.serialized for action in sorted(self.actions, key=lambda a: a.price_by_profit)]
        self.name = "TOTAL"
        data.append(self.serialized)
        df = pandas.DataFrame(data)
        return df.to_string(index=False)

    def _sum_attribute(self, key):
        """ Make the sum of an attribute from all actions. """
        sum_ = 0
        for action in self.actions:
            sum_ += object.__getattribute__(action, key)
        return sum_

    def calculate_price(self):
        """ Calculate an actions group total price. """
        return self._sum_attribute("price")

    def calculate_profit(self):
        """ Calculate an actions group total profit. """
        return self._sum_attribute("profit")

    def calculate_price_by_profit(self):
        """ Calculate an actions group price by profit. """
        return self.price / self.profit
