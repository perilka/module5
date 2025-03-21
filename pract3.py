import itertools


class Card:
    def __init__(self, cardtype, suit):
        self.suit = suit
        self.type = cardtype

    def __str__(self):
        return f'{self.type} of {self.suit}'


cardtypes = [str(i) for i in range(2, 11)] + ['Jack', 'Queen', 'King', 'Ace']
suits = ['Diamonds', 'Hearts', 'Spades', 'Clubs']


cards_list = []
for cardtype in cardtypes:
    for suit in suits:
        card = Card(cardtype=cardtype, suit=suit)
        cards_list.append(str(card))

print(cards_list)


cards_combinations = itertools.permutations(cards_list)

with open('all_combinations.txt', 'w', encoding='utf8') as f:
    for comb in cards_combinations:
        for card in comb:
            f.write(card + ' ')
        f.write('\n')