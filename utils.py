from functools import cached_property
import pandas


# Displays int XOR floats rounded to two decimal places.
pandas.options.display.float_format = lambda n: str(int(n)) if int(n) == n else "{:.2f}".format(n)


class Action:
    """ An object to access to actions properties easily. """
    def __init__(self, name: str, price: str, profit: str):
        self.name = name
        self.price = float(price)
        self.profit_percentage = float(profit)
        self.profit = self.price * self.profit_percentage / 100

    def __str__(self):
        return f"{self.name}({self.price}€) => +{self.profit}€"

    @cached_property
    def serialized(self):
        to_serialize = ["name", "price (€)", "profit (€)"]
        return {key.capitalize(): object.__getattribute__(self, key.replace(" (€)", "")) for key in to_serialize}


class Group:
    """ An object to access a resume of several actions, their total cost and total profit. """
    def __init__(self, actions: list[Action]):
        self.actions = actions
        self.price = self.calculate_price()
        self.profit = self.calculate_profit()

    def __str__(self):
        data = [action.serialized for action in self.actions]
        data.append({"Name": "TOTAL", "Price (€)": self.price, "Profit (€)": self.profit})
        df = pandas.DataFrame(data)
        return df.to_string(index=False)

    def calculate_price(self):
        """ Calculate an actions group total price. """
        price = 0
        for action in self.actions:
            price += action.price
        return price

    def calculate_profit(self):
        """ Calculate an actions group total profit. """
        profit = 0
        for action in self.actions:
            profit += action.profit
        return profit
