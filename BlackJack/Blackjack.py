from dataclasses import dataclass
import random

player1_score = 0
dealers_score = 0


@dataclass
class BlackJackGame:
    pulled_card = ""
    ace_card = {"A": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10,"K": 10}

    card = {"A": 11, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10,"K": 10}
    cards = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    dealers_cards = []
    player1_cards = []
    player1_cards1 = []
    player1_cards2 = []
    ace = False

    player1_score = player1_score
    dealers_score = dealers_score
    game_running = True

    def card_pull(self):
        self.pulled_card = self.cards[random.randint(0,12)]
        return self.pulled_card

    def setup(self):
        self.game_running = True
        for i in range(2):
            self.player1_cards.append(self.card_pull())
        self.check_win()
        self.dealers_cards.append(self.card_pull())
        self.decoder(self.dealers_cards)
        print(f"dealers cards are {self.dealers_cards}")

    def dealer(self):
        self.dealers_cards.append(self.card_pull())
        self.decoder(self.dealers_cards)
        print(f"dealers cards are {self.dealers_cards}")
        while sum(self.decoder(self.dealers_cards)) < 15:
            self.dealers_cards.append(self.card_pull())
            print(f"dealers cards are{self.dealers_cards}")
            self.check_win()

    def decoder(self,main_card):
        if self.ace is True:
            decoded = ([self.ace_card.get(card) for card in main_card])
        else:
            decoded = ([self.card.get(card) for card in main_card])
        return decoded

    def player1(self):
        print(f"player 1's cards are {self.player1_cards}")
        print(f'you have a total of {sum(self.decoder(self.player1_cards))}')
        for ace in self.player1_cards:
            if ace == "A" and sum(self.decoder(self.player1_cards)) > 21:
                self.ace = True
        if sum(self.decoder(self.player1_cards)) >= 17 and self.ace == True:
            while sum(self.decoder(self.player1_cards)) < 17:
                option1 = input("do you want to hit or stand? ")
                if option1 == "hit":
                    self.player1_cards.append(self.card_pull())
                    print(self.player1_cards)
                    if sum(self.decoder(self.player1_cards)) < 21:
                       print(f"you now have a total of {sum(self.decoder(self.player1_cards))}")
                else:
                    continue
        elif sum(self.decoder(self.player1_cards)) >= 17:
            print(sum(self.decoder(self.player1_cards)))
            print("you cant hit since your 17 or above")
        else:
            while sum(self.decoder(self.player1_cards)) < 17:
                option1 = input("do you want to hit or stand? ")
                if option1 == "hit":
                    self.player1_cards.append(self.card_pull())
                    print(self.player1_cards)
                    if sum(self.decoder(self.player1_cards)) < 21:
                       print(f"you now have a total of {sum(self.decoder(self.player1_cards))}")
        self.check_win()

    def check_win(self):
        if sum(self.decoder(self.player1_cards)) > 21:
            print(f"dealer wins because player 1 busted {sum(self.decoder(self.player1_cards))}")
            self.dealers_score += 1
            self.game_running = False
        elif sum(self.decoder(self.dealers_cards)) > 21:
            print("player 1 wins because the dealer busted")
            self.player1_score += 1
            self.game_running = False

        elif sum(self.decoder(self.player1_cards)) == 21:
            print("player 1 wins by blackjack")
            self.player1_score += 1
            self.game_running = False

        elif sum(self.decoder(self.dealers_cards)) == 21:
            print("dealer wins by blackjack")
            self.dealers_score += 1
            self.game_running = False
    def final_win_check(self):
        if sum(self.decoder(self.player1_cards)) > sum(self.decoder(self.dealers_cards)):
            print("player 1 wins")
            self.player1_score += 1
            self.game_running = False

        elif sum(self.decoder(self.player1_cards)) == sum(self.decoder(self.dealers_cards)):
            print("its a tie")
            self.game_running = False

        elif sum(self.decoder(self.player1_cards)) < sum(self.decoder(self.dealers_cards)):
            print("dealer wins")
            self.game_running = False


    def runner(self):
        self.player1()
        self.check_win()
        while sum(self.decoder(self.dealers_cards)) >= 17 and sum(self.decoder(self.player1_cards)) >= 17:
            self.final_win_check()
            break



if __name__ == "__main__":
    BlackJackGame().setup()
    BlackJackGame().runner()
    BlackJackGame().final_win_check()

