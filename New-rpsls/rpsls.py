from dataclasses import dataclass

@dataclass
class GameTwo:
    one, two = "",""
    def get_move(self):
        self.one = str(input("rock, paper, scissors, lizard, spock (p1): "))
        self.two = str(input("rock, paper, scissors, lizard, spock (p2): "))
    def win_check(self):
        if self.one == "rock":
            if self.two == "paper" or self.two == "spock":
                print(f"{self.two} beats {self.one}, player 2 wins")
            if self.two == "lizard" or self.two == "scissors":
                print(f"{self.one} beats {self.two}, player 1 wins")
            if self.one == self.two:
                print("Its a Tie")
        if self.one == "paper":
            if self.two == "lizard" or self.two == "scissors":
                print(f"{self.two} beats {self.one}, player 2 wins")
            if self.two == "spock" or self.two == "rock":
                print(f"{self.one} beats {self.two}, player 1 wins")
            if self.one == self.two:
                print("Its a Tie")
        if self.one == "scissors":
            if self.two == "spock" or self.two == "rock":
                print(f"{self.two} beats {self.one}, player 2 wins")
            if self.two == "paper" or self.two == "lizard":
                print(f"{self.one} beats {self.two}, player 1 wins")
            if self.one == self.two:
                print("Its a Tie")
        if self.one == "lizard":
            if self.two == "scissors" or self.two == "rock":
                print(f"{self.two} beats {self.one}, player 2 wins")
            if self.two == "spock" or self.two == "paper":
                print(f"{self.one} beats {self.two}, player 1 wins")
            if self.one == self.two:
                print("Its a Tie")
        if self.one == "spock":
            if self.two == "paper" or self.two == "lizard":
                print(f"{self.two} beats {self.one}, player 2 wins")
            if self.two == "scissors" or self.two == "rock":
                print(f"{self.one} beats {self.two}, player 1 wins")
            if self.one == self.two:
                print("Its a Tie")
    def check_n_play(self):
        self.get_move()
        self.win_check()


if __name__ == "__main__":
    play = GameTwo()
    play.check_n_play()