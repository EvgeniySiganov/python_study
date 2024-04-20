import os
import tempfile
import json


class Transaction:
    def __init__(self, summ: int, date: str = None, currency: str = "USD", rate_against_dollar: float = 1.0,
                 description: str = None):
        self.__summ = summ
        self.__date = date
        self.__currency = "USD" if currency is None or not currency else currency
        self.__rate_against_dollar = rate_against_dollar if rate_against_dollar else 1.0
        self.__description = description

    def amount(self):
        return self.__summ

    def date(self):
        return self.__date

    def currency(self):
        return self.__currency

    def usd_conversion_rate(self):
        return self.__rate_against_dollar

    def description(self):
        return self.__description

    def usd(self):
        return self.__summ * self.__rate_against_dollar


class Account:

    def __init__(self, number: str = None, name: str = None, transactions_list: list = None):
        self.__number = number
        self.__name = name
        self.__transactions = transactions_list
        self.path = os.path.join(tempfile.gettempdir(), self.__number)

    def number(self):
        return self.__number

    def get_name(self):
        return self.__name

    def set_name(self, name):
        if len(name) > 3:
            self.__name = name
        else:
            error = f"invalid name {name}, minimum amount of letters is 4."
            raise ValueError(error)

    def __len__(self):
        return len(self.__transactions)

    def balance(self):
        return sum(t.amount() * t.usd_conversion_rate() for t in self.__transactions)

    def all_usd(self):
        return all(t.currency() == "USD" for t in self.__transactions)

    def apply(self, transaction):
        self.__transactions.append(transaction)

    def account_encoder(self):
        return {
            "number": self.__number,
            "name": self.__name,
            "transactions": [t.__dict__ for t in self.__transactions]
        }

    def save(self):
        json_obj = self.account_encoder()
        json_string = json.dumps(json_obj)
        json_bytes = json_string.encode("utf-8")
        with open(self.path, "wb") as file:
            file.write(json_bytes)
        print(f"saved to {self.path}")

    def load(self):
        with open(self.path, "r") as file:
            json_loaded = json.load(file)
        return json_loaded


transaction1 = Transaction(summ=100)
transaction2 = Transaction(summ=200)
transactions = [transaction1, transaction2]
account = Account(number="123", name="black", transactions_list=transactions)
account.save()
print(account.load())
