from dataclasses import dataclass
import random

@dataclass
class BlackJackGame:
    pulled_card = ""
    card = {"A": 11, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10, "K": 10}
    cards = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
    dealers_cards = []
    player1_cards = []
    player1_score = 0
    dealers_score = 0


    def card_pull(self):
        self.pulled_card = self.cards[random.randint(0,12)]
        return self.pulled_card

    def dealer(self):
        for i in range(2):
            self.dealers_cards.append(self.card_pull())
        self.decoder(self.dealers_cards)
        print(f"dealers cards are {self.dealers_cards}")

    def decoder(self,main_card):
        decoded = ([self.card.get(card) for card in main_card])
        return decoded

    def player1(self):
        for i in range(2):
            self.player1_cards.append(self.card_pull())
        print(f"player 1's cards are {self.player1_cards}")
        if sum(self.decoder(self.player1_cards)) >= 17:
            print(sum(self.decoder(self.player1_cards,)))
            print("you cant hit since your 17 or above")
            self.player1_cards.append(self.card_pull())
        else:
            option1 = input("do you want to hit or pass? ")
            if option1 == "hit":
                self.player1_cards.append(self.card_pull())
                print(self.player1_cards)
                if sum(self.decoder(self.player1_cards)) < 21:
                    print(f"you now have a total of {sum(self.decoder(self.player1_cards))}")
                self.check_win()

    def check_win(self):
        if sum(self.player1_cards) > 21:
            print("dealer wins because player 1 busted")

        elif sum(self.dealers_cards) > 21:
            print("player 1 wins because the dealer busted")

        elif sum(self.player1_cards) == 21 and sum(self.dealers_cards) == 21:
            print("its a tie of blackjack")

        elif sum(self.player1_cards) == 21:
            print("player 1 wins by blackjack")

        elif sum(self.dealers_cards) == 21:
            print("dealer wins by blackjack")

        elif sum(self.player1_cards) > sum(self.dealers_cards):
            print("player 1 wins")

        elif sum(self.player1_cards) == sum(self.dealers_cards):
            print("its a tie")

        elif sum(self.player1_cards) < sum(self.dealers_cards):
            print("dealer wins")

    def runner(self):
        self.dealer()
        self.player1()


if __name__ == "__main__":
    BlackJackGame().runner()