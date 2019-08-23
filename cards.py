import random

# cards = []

class Card:
    def __init__(self, num, suit, value):
        self.num = num
        self.suit = suit
        self.disp = num + suit
        self.value = value

class Stack:
    def __init__(self):
        self.hand = []
        
    def add_card(self,card):
        self.hand.append(card)

    def play_card(self,card):
        return self.hand.pop(card)

    def show_hand(self):
        card_str = ""
        for i in self.hand:
            card_str += i.disp + ", "
        return card_str[:-2]

    def has_suit(self,suit):
        for i in self.hand:
            if i.suit == suit:
                return True

    def has_number(self,number):
        for i in self.hand:
            if i.number == number:
                return True

    def has_value(self,value):
        for i in self.hand:
            if i.value == value:
                return True

class Deck(Stack):
    def __init__(self,numbers=False,suits=False):
        super().__init__()
        if numbers and suits:
            self.build(numbers,suits)

    def build(self,numbers,suits):
        for i in numbers:
            k = numbers[i]
            for j in suits:
                self.add_card(Card(i,j,k))

    def shuffle(self):
        random.shuffle(self.hand)

    def take(self,i=0):
        return self.play_card(i)

# create and shuffle deck

def build_standard_deck(jokers=True):
    numbers = {"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,
               "X":10,"J":11,"Q":12,"K":13,"A":14}
    suits = ["H", "D", "S", "C"]
    
    d = Deck(numbers,suits)

    if jokers:
        d.add_card(Card("J","*",0))
        d.add_card(Card("J","*",0))
        
    return d

def build_7_low_deck():
    numbers = {"7":7,"8":8,"9":9,"X":10,"J":11,"Q":12,"K":13,"A":14}
    suits = ["H", "D", "S", "C"]

    d = Deck(numbers,suits)

    d.add_card(Card("J","*",6))

    return d
