class Card:
    def __init__(self, number, holder, valid_date, ccv):
        self.number = number
        self.holder = holder
        self.valid_date = valid_date
        self.ccv = ccv

    def get_hidden_number(self):
        return '{}** **** **** {}'.format(self.number[:2], self.number[-4:])


class MasterCard(Card):
    def __str__(self):
        return '[mastercard {}]'.format(self.get_hidden_number())


class Visa(Card):
    def __str__(self):
        return '[visa {}]'.format(self.get_hidden_number())


# [mastercard 12** **** **** 3456]
# [visa 12** **** **** 3456]
print(MasterCard('1234567890123456', 'Vasia', '12.12.2024', '1234'))
print(Visa('1234567890123456', 'Vasia', '12.12.2024', '1234'))
