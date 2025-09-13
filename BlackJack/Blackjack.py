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

    player1_score = player1_score
    dealers_score = dealers_score
    game_running = True

    def split_check(self, check_list):
        print('checking for split')
        if len(check_list) == 2:
            p1 = check_list[0]
            p2 = check_list[1]
            p3 = sum(self.card.get(card) for card in p1)
            p4 = sum(self.card.get(card) for card in p2)
            print('first check done')
            if p3 == p4:
                return True
        else:
            return False



    def card_pull(self):
        self.pulled_card = self.cards[random.randint(0,12)]
        return self.pulled_card


    def setup(self):
        self.game_running = True
        for i in range(2):
            self.player1_cards.append(self.card_pull())
        if sum(self.decoder(self.player1_cards)) == 21:
            self.dealers_cards.append(self.card_pull())
            self.decoder(self.dealers_cards)
            print(f"dealers cards are {self.dealers_cards} with a total of {sum(self.decoder(self.dealers_cards))}")
            print(f"player 1's cards are {self.player1_cards}")
            print(f'you have a total of {sum(self.decoder(self.player1_cards))}')
            print("player 1 wins by blackjack")
            self.player1_score += 1
            self.game_running = False

        else:
            self.dealers_cards.append(self.card_pull())
            self.decoder(self.dealers_cards)
            print(f"dealers cards are {self.dealers_cards} with a total of {sum(self.decoder(self.dealers_cards))}")
            print(f"player 1's cards are {self.player1_cards}")
            print(f'you have a total of {sum(self.decoder(self.player1_cards))}')

            self.runner()




    def dealer(self):
        self.dealers_cards.append(self.card_pull())
        self.decoder(self.dealers_cards)
        print(f"dealers cards are {self.dealers_cards} with a total of {sum(self.decoder(self.dealers_cards))}")
        while sum(self.decoder(self.dealers_cards)) < 17:
            self.dealers_cards.append(self.card_pull())
            print(f"dealers cards are{self.dealers_cards} with a total of {sum(self.decoder(self.dealers_cards))}")


    def decoder(self,main_card):
        if sum([self.card.get(card) for card in main_card]) > 21:
            decoded = ([self.ace_card.get(card) for card in main_card])
        else:
            decoded = ([self.card.get(card) for card in main_card])
        return decoded

    def run_split(self, cards, new_card):
        spliter = input('do you want to split?')
        if spliter == 'yes' or spliter == 'split':
            adder = cards[1]
            cards.remove(cards[1])
            new_card.append(adder)
            print(f'{cards}')
            return cards, new_card


    def player1(self):
        while self.game_running is True :
            if self.split_check(self.player1_cards) is True:
                self.run_split(self.player1_cards, self.player1_cards1)
            option1 = input("do you want to hit or stand? ")
            if option1 == "hit":
                self.player1_cards.append(self.card_pull())
                print(self.player1_cards)
                print(f'you have a total of {sum(self.decoder(self.player1_cards))}')
                self.check_win()
                if sum(self.decoder(self.player1_cards)) < 21:
                    print(f"you now have a total of {sum(self.decoder(self.player1_cards))}")
            else:
                break



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
        if self.game_running is True:
            self.dealer()
            self.check_win()

        if self.game_running is True:
            self.final_win_check()




if __name__ == "__main__":
    BlackJackGame().setup()

