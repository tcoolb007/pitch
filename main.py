import cards
import pdb

# define class 'Player'

class Team():
    def __init__(self,name,t1,t2):
        self.name = name
        self.t1 = t1
        self.t2 = t2
        self.pile = []
        self.trump_pile = []
        self.points = 0
        self.pts_queue = 0

        t1.join_team(self)
        t2.join_team(self)

    def build_pile(self):
        self.pile += self.t1.pile + self.t2.pile

    def build_trump_pile(self):
        for i in self.pile:
            if i.suit == trump:
                self.trump_pile.append(i)

    def count_game(self):
        game = 0
        for i in self.pile:
            if i.value == 10:
                game += 10
            elif i.value > 10:
                game += i.value - 10
        return game
    
    def add_pts(self,pts):
        self.pts_queue += pts

    def set_pts(self,pts):
        self.pts_queue = pts

    def win_pts(self):
        self.points += self.pts_queue

    def show_pile(self):
        card_str = ""
        for i in self.pile:
            card_str += i.disp + ", "
        return card_str[:-2]

    def show_trump_pile(self):
        card_str = ""
        for i in self.trump_pile:
            card_str += i.disp + ", "
        return card_str

class Player(cards.Stack):
    def __init__(self, name, pid):
        super().__init__()
        self.pile = []
        self.name = name
        self.pid  = pid
        self.team = None

    def join_team(self, team):
        self.team = team

    def win_card(self, card):
        self.pile.append(card)

    def show_pile(self):
        card_str = ""
        for i in self.pile:
            card_str += i.disp + ", "
        return card_str
    
def deal():
    for i in range(6):
        p1.add_card(deck.take())
        p2.add_card(deck.take())
        p3.add_card(deck.take())
        p4.add_card(deck.take())

# DEFINITIONS FOR PLAYERS / TEAMS / DECK
p1 = Player("P1",1)
p2 = Player("P2",2)
p3 = Player("P3",3)
p4 = Player("P4",4)
players = [p1,p2,p3,p4,p1,p2,p3]

team1 = Team("Team 1",p1,p3)
team2 = Team("Team 2",p2,p4)

# set up cards
deck = cards.build_7_low_deck()
deck.shuffle()

deal()

# global variables trump, led suit, leading player
trump = ""
led   = ""
leader= p1
dealer= p1

# cards currently on table
trick_cds = {}

def input_number(prompt):
    inpt = input(prompt)
    try:
        return int(inpt)
    except ValueError:
        print("Please enter a number")
        return input_number(prompt)        

def show_trick():
    card_str = "| "
    for i in trick_cds.values():
        card_str += i.disp + " | "
    return card_str

def reset_trick():
    global led
    global trick_cds

    led = ""
    trick_cds = {}

    team1.win_pts()
    team2.win_pts()

def reset_hand():
    global trump, deck
    trump = ""
    
    reset_trick()

    pdb.set_trace()
    deck = cards.build_7_low_deck()
    deck.shuffle()
    deal()

def do_bidding(start):
    # bidding serves to choose leader and bid
    global leader, bid

    # dummy bid
    bid = 0
    bid_winner = p4

# TODO: dealer can take without raising

    for j in range(4):
        i = j + start.pid - 1 # player currently bidding
        bid_good = False # variable to check whether bid is good
        while True:
            bid_inpt = input_number(f"{players[i].name} bid \
({players[i].show_hand()})({bid}): ")
            # reject bids less than current highest, any bid > 6, or = 1
            if (bid_inpt < bid and not bid_inpt == 0)\
                    or (bid_inpt > 6) or (bid_inpt == 1):
                print("Invalid bid")
            else:
                break
                print(f"{players[i].name} bids {bid_inpt}")
        if bid_inpt > bid and bid_inpt >= 2:
            bid = bid_inpt
            leader = players[i]

    if bid == 0:
        bid = 2
        leader = players[leader.pid + 1]

    print(f"{leader.name} takes it for {bid}!")

def trick_play_card(player):
    # TODO: currently, the first card cannot be played because trump has
    # not been set. exception needs to be made for the first card of each
    # HAND (not trick)
    global trick_cds
    
    inpt = input_number(f"{player.name}({player.show_hand()}): ") - 1
    #while True:
     #   inpt = input_number(f"{player.name}({player.show_hand()}): ") - 1
      #  if inpt >= 0 and inpt < len(player.hand):
       #     print("valid card")
        #    break
    #    else:
     #       print("Invalid card!")
    
    #while True:
     #   if player.hand[inpt].suit == led or \
      #     player.hand[inpt].suit == trump: # don't bother checking hand
       #     break
    #    elif player.has_suit(led) or player.has_suit(trump) or player.has_suit("*"):
     #       print("Invalid card!")
      #      inpt = trick_play_card(player)

    trick_cds[player.name] = player.play_card(inpt) # play valid card
    return inpt
        
def do_trick(trick_nm,leader):
    # start with `leader`
    lead_nm = leader.pid
    t1 = players[lead_nm - 1]
    t2 = players[lead_nm]
    t3 = players[lead_nm + 1]
    t4 = players[lead_nm + 2]
    
    # play first card
    trick_play_card(t1)

    # set trump and suit
    global led
    global trump

    led = trick_cds.get(t1.name).suit
    if (trick_nm == 0):
        trump = led

    print(f"Trump: {trump}")
    print(show_trick())

    # play remaining cards
    trick_play_card(t2)
    print(show_trick())
    trick_play_card(t3)
    print(show_trick())
    trick_play_card(t4)
    print(show_trick())

def score_trick():
    # calculate winner of trick
    global trump, led
    global leader
    
    # dummy card to compare others to
    high_cd = cards.Card("0","0",1)
    
    # check for any trump (or joker), and if there is any, choose the highest
    for i in trick_cds:
        cd = trick_cds.get(i)
        if cd.suit == trump or cd.suit == "*":
            if cd.value > high_cd.value:
                high_cd = cd
    # if there is no trump, choose the highest card of the suit led
    if high_cd.value == 1:
        for i in trick_cds:
            cd = trick_cds.get(i)
            if cd.suit == led:
                if cd.value > high_cd.value:
                    high_cd = cd
    trick_winner = ""
    for i,j in trick_cds.items():
        if j == high_cd:
            if i == p1.name:
                trick_winner = p1
            elif i == p2.name:
                trick_winner = p2
            elif i == p3.name:
                trick_winner = p3
            elif i == p4.name:
                trick_winner = p4
    # declare winner
    print(trick_winner.name + " wins this trick.")
    leader = trick_winner

    for i in trick_cds:
        trick_winner.win_card(trick_cds.get(i))

    reset_trick()

    print(p1.name)
    print(p1.show_pile())
    print(p2.name)
    print(p2.show_pile())
    print(p3.name)
    print(p3.show_pile())
    print(p4.name)
    print(p4.show_pile())

def update_score():
    global bid

    # compare highest bidder's score to their bid
    if leader.team.pts_queue >= bid:
        print(f"{leader.team.name} met their bid and get {leader.team.pts_queue} points")
    else:
        print(f"{leader.team.name} got set {bid} points!")
        leader.team.set_pts(-bid)

    team1.win_pts()
    team2.win_pts()

def do_hand(dealer):
    print(f"{dealer.name} deals")
    
    do_bidding(players[dealer.pid])
    
    # do 6 tricks
    for i in range(6):
        do_trick(i,leader)
        score_trick()

    # combine partner's piles
    team1.build_pile()
    team2.build_pile()

    # get list of trump cards in pile
    team1.build_trump_pile()
    team2.build_trump_pile()
    
    # count high
    high_cd_1 = 0
    for i in team1.trump_pile:
        if i.value > high_cd_1:
            high_cd_1 = i.value

    high_cd_2 = 0
    for i in team2.trump_pile:
        if i.value > high_cd_2:
            high_cd_2 = i.value

    if high_cd_1 > high_cd_2:
        print(f"Point for high to {team1.name}")
        team1.add_pts(1)
    else:
        print(f"Point for high to {team2.name}")
        team2.add_pts(1)

    # count low
    low_cd_1 = 15
    for i in team1.trump_pile:
        if i.value < low_cd_1:
            low_cd_1 = i.value

    low_cd_2 = 15
    for i in team2.trump_pile:
        if i.value < low_cd_2:
            low_cd_2 = i.value

    if low_cd_1 < low_cd_2:
        print(f"Point for low to {team1.name}")
        team1.add_pts(1)
    else:
        print(f"Point for low to {team2.name}")
        team2.add_pts(1)

    # count jack
    for i in team1.trump_pile:
        if i.value == 11:
            print(f"Point for jack to {team1.name}")
            team1.add_pts(1)
            break

    for i in team2.trump_pile:
        if i.value == 11:
            print(f"Point for jack to {team2.name}")
            team2.add_pts(1)
            break

    # count game in each pile
    game_a = team1.count_game()
    game_b = team2.count_game()
    
    if game_a > game_b:
        print(f"Point for game to {team1.name}")
        team1.add_pts(1)
    elif game_b > game_a:
        print(f"Point for game to {team2.name}")
        team2.add_pts(1)

    # count joker
    for i in team1.pile:
        if i.suit == "*":
            print(f"Points for joker to {team1.name}")
            team1.add_pts(2)
            break

    for i in team2.pile:
        if i.suit == "*":
            print(f"Point for joker to {team2.name}")
            team2.add_pts(2)
            break
    print(f"HAND SCORE: T1:{team1.pts_queue} T2: {team2.pts_queue}")
    print(f"BID: {bid}")

    update_score()

    print(f"TOTAL SCORE: T1:{team1.points} T2: {team2.points}")
    
def do_game():
    global dealer
    
    do_hand(p1) # do first hand
    
    while team1.points < 21 and team2.points < 21: # do all other hands
        reset_hand()
        dealer = players[dealer.pid]
        print("\n\n\nNEW HAND")
        do_hand(dealer)

    if team1.points > 21:
        print(f"{team1.name} wins!")
    else:
        print(f"{team2.name} wins!")

do_game()
