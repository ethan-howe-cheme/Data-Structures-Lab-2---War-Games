from typing import List, Optional
from functools import total_ordering, reduce
import csv
import os
import random


class Player:
    """A Chemist in the game of Chemical Stack!"""
    name: str
    wins: int

    def __init__(self, name: str):
        self.name = name
        self.wins = 0

    def get_name(self) -> str:
        return self.name

    def get_wins(self) -> int:
        return self.wins

    def note_win(self):
        self.wins = self.wins + 1

    def __lt__(self, other: 'Player') -> bool:
        if self.get_wins() < other.get_wins():
            return True
        else:
            return False

@total_ordering
class Chemical:
    """A chemical composed of multiple elements."""

    _name: str
    _contents: List["Element"]

    def __init__(self, name: str = "") -> None:
        self._name = name
        self._contents = []

    def name(self) -> str:
        return self._name

    def mass(self) -> float:
        return reduce(lambda c, n: c + n.mass(), self._contents, 0)

    def __add__(self, other: "Element") -> "Chemical":
        a = Chemical(self._name)
        a._contents = self._contents.copy()
        a._contents.append(other)
        return a

    def __repr__(self) -> str:
        return f"{self._name if self._name else 'Chemical'} is composed of " + ", ".join(
            map(lambda c: repr(c), self._contents)
        )

    def __lt__(self, other: "Chemical") -> bool:
        return self.mass() < other.mass()


class Element:
    """A chemical element."""

    _name: str
    _mass: float

    def __init__(self, name: str, atomic_mass: float) -> None:
        self._name = name
        self._mass = atomic_mass

    def name(self) -> str:
        return self._name

    def mass(self) -> float:
        return self._mass

    def __repr__(self) -> str:
        return f"{self.name()} (mass: {self.mass()})"

    def __add__(self, other: "Element") -> Chemical:
        c = Chemical()
        c._contents = [self, other]
        return c


class PeriodicTable:
    """The Periodic Table of elements."""

    _table: List[Element]

    def __init__(self, filename: str):
        self._table = []
        with open(filename, mode="r") as f:
            for l in csv.reader(f):
                element = Element(l[2], float(l[3]))
                self._table.append(element)

    def random(self) -> Optional[Element]:
        if len(self._table) == 0:
            return None
        r = random.randint(0, len(self._table) - 1)
        self._table[-1], self._table[r] = self._table[r], self._table[-1]
        try:
            return self._table.pop()
        except IndexError as e:
            return None


class Game:
    """A game of Chemical Stack!"""

    _players: List[Player]
    _stack: List[Element]
    player1_deck = List[Element]
    player2_deck = List[Element]
    p1_rounds = 0
    p2_rounds = 0
    p1_biggest_stack = 0
    p2_biggest_stack = 0

    #Tiebreaker chemicals in descending rank (TiC, FeS2, NaHCO3, NaCl, H2O)
    #These can be changed (or new ones added) by the user if they want, as long as the list stays in descending rank
    TieBreakerChemicals = [
        Chemical("TiC") + Element("Titanium", 47.867) + Element("Carbon", 12.011),
        Chemical("FeS2") + Element("Iron", 55.84) + Element("Sulfur", 32.07) + Element("Sulfur", 32.07),
        Chemical("NaHCO3") + Element("Sodium", 22.9897693) + Element("Hydrogen", 1.0080) + Element("Carbon", 12.011)
            + Element("Oxygen", 15.999) + Element("Oxygen", 15.999) + Element("Oxygen", 15.999),
        Chemical("NaCl") + Element("Sodium", 22.9897693) + Element("Chlorine", 35.45),
        Chemical("H2O") + Element("Hydrogen", 1.0080) + Element("Hydrogen", 1.0080) + Element("Oxygen", 15.999),
    ]

    def __init__(self, p1: Player, p2: Player):
        self._players = [p1, p2]
        self.p1_biggest_elements = []
        self.p2_biggest_elements = []
        self._stack = []
        self.player1_deck = []
        self.player2_deck = []
        game_deck = PeriodicTable(os.path.join(os.path.dirname(os.path.abspath(__file__)), "periodic.csv"))

        print(f"NEW GAME: {self._players[0].get_name()} vs {self._players[1].get_name()}!")

        for pdecks in range(55):
            self.player1_deck.append(game_deck.random())
            self.player2_deck.append(game_deck.random())
        for sdeck in range(8):
            self._stack.append(game_deck.random())


    def decks_and_stack(self):
        print(f"{self._players[0].get_name()}'s deck: {self.player1_deck}")
        print(f"\n{self._players[1].get_name()}'s deck: {self.player2_deck}")
        print(f"\nStack: {self._stack}\n")



    def play_round(self, round: int):
        p1_points = 0
        p2_points = 0
        stack_element = self._stack[round]

        #search through each player deck (player1/2_deck) and find stackable elements for round's element (count using points)
        #an element is stackable if its starting letter matches the stack element's or its mass is within +/- 10 amu
        #each element is a "card" that can only be stacked once per round (1 point even if it matches both ways)
        #cards are not removed from the decks, so players get them back for the next round
        for element in self.player1_deck:
            if element.name()[0] == stack_element.name()[0] or abs(element.mass() - stack_element.mass()) <= 10:
                p1_points += 1

        for element in self.player2_deck:
            if element.name()[0] == stack_element.name()[0] or abs(element.mass() - stack_element.mass()) <= 10:
                p2_points += 1

        #track each player's biggest stack of the game for stats (every stack element is kept if tied)
        if p1_points > self.p1_biggest_stack:
            self.p1_biggest_stack = p1_points
            self.p1_biggest_elements = [stack_element]
        elif p1_points == self.p1_biggest_stack:
            self.p1_biggest_elements.append(stack_element)
        if p2_points > self.p2_biggest_stack:
            self.p2_biggest_stack = p2_points
            self.p2_biggest_elements = [stack_element]
        elif p2_points == self.p2_biggest_stack:
            self.p2_biggest_elements.append(stack_element)

        if p1_points > p2_points:
            print(f"Round {round + 1}: {self._players[0].get_name()} wins this round!")
            self.p1_rounds += 1

        elif p2_points > p1_points:
            print(f"Round {round + 1}: {self._players[1].get_name()} wins this round!")
            self.p2_rounds += 1
        else:
            print(f"Round {round + 1}: This round is a tie!")

    def play_tiebreaker(self):
        #players create chemicals from TieBreakerChemicals (highest rank first) using the elements in their decks
        p1_tb = 0
        p2_tb = 0
        p1_names = [element.name() for element in self.player1_deck]
        p2_names = [element.name() for element in self.player2_deck]
        p1_chemicals = []
        p2_chemicals = []

        print("Tiebreaker chemicals (highest rank first):")
        for rank in range(len(self.TieBreakerChemicals)):
            print(f"{rank + 1}. {self.TieBreakerChemicals[rank]}")

        #a player can make a chemical if they hold every element in it (one of each element is enough)
        for chemical in self.TieBreakerChemicals:
            if all(element.name() in p1_names for element in chemical._contents):
                p1_chemicals.append(chemical)
            if all(element.name() in p2_names for element in chemical._contents):
                p2_chemicals.append(chemical)

        print(f"\n{self._players[0].get_name()} can make: {', '.join(chemical.name() for chemical in p1_chemicals) if p1_chemicals else 'none'}")
        print(f"{self._players[1].get_name()} can make: {', '.join(chemical.name() for chemical in p2_chemicals) if p2_chemicals else 'none'}")

        #the higher ranked best chemical wins (top of the list scores the most)
        if len(p1_chemicals) > 0:
            p1_tb = len(self.TieBreakerChemicals) - self.TieBreakerChemicals.index(p1_chemicals[0])
        if len(p2_chemicals) > 0:
            p2_tb = len(self.TieBreakerChemicals) - self.TieBreakerChemicals.index(p2_chemicals[0])

        #if neither player can make a chemical, the player with the highest mass noble gas wins
        #if every noble gas is in the stack, Gold then Silver decide the winner
        if p1_tb == 0 and p2_tb == 0:
            deciding_elements = ["Oganesson", "Radon", "Xenon", "Krypton", "Argon", "Neon", "Helium", "Gold", "Silver"]
            for deciding in deciding_elements:
                if deciding in p1_names or deciding in p2_names:
                    if deciding in p1_names:
                        p1_tb = 1
                    else:
                        p2_tb = 1
                    print(f"No chemicals can be made, so {deciding} decides the winner!")
                    break

        if p1_tb > p2_tb:
            print(f"\n{self._players[0].get_name()} wins the game!")
            self._players[0].note_win()
        else:
            print(f"\n{self._players[1].get_name()} wins the game!")
            self._players[1].note_win()


    def play(self):
        for round in range(8):

            self.play_round(round)

        if self.p1_rounds == self.p2_rounds:
            print("\nTiebreaker!")
            self.play_tiebreaker()
        elif self.p1_rounds > self.p2_rounds:
            print(f"\n{self._players[0].get_name()} wins the game winning {self.p1_rounds} rounds!")
            self._players[0].note_win()
        else:
            print(f"\n{self._players[1].get_name()} wins the game winning {self.p2_rounds} rounds!")
            self._players[1].note_win()

    def stats(self):
        #best chemical each player could make with their deck from the previous game (first one found is highest rank)
        p1_names = [element.name() for element in self.player1_deck]
        p2_names = [element.name() for element in self.player2_deck]
        p1_best = None
        p2_best = None
        for chemical in self.TieBreakerChemicals:
            if p1_best is None and all(element.name() in p1_names for element in chemical._contents):
                p1_best = chemical
            if p2_best is None and all(element.name() in p2_names for element in chemical._contents):
                p2_best = chemical

        print("\nStats:")
        print(f"{self._players[0].get_name()}")
        print(f"  Total Wins: {self._players[0].get_wins()}")
        print(f"  Rounds Won: {self.p1_rounds}")
        print(f"  Best Chemical: {p1_best.name() if p1_best is not None else 'none'}")
        print(f"  Biggest Stack: {self.p1_biggest_stack} elements on {', '.join(repr(element) for element in self.p1_biggest_elements)}")
        print(f"\n{self._players[1].get_name()}")
        print(f"  Total Wins: {self._players[1].get_wins()}")
        print(f"  Rounds Won: {self.p2_rounds}")
        print(f"  Best Chemical: {p2_best.name() if p2_best is not None else 'none'}")
        print(f"  Biggest Stack: {self.p2_biggest_stack} elements on {', '.join(repr(element) for element in self.p2_biggest_elements)}\n\n")

    def reset(self):
        self.p1_rounds = 0
        self.p2_rounds = 0
        self.p1_biggest_stack = 0
        self.p2_biggest_stack = 0
        self.p1_biggest_elements = []
        self.p2_biggest_elements = []
        game_deck = PeriodicTable(os.path.join(os.path.dirname(os.path.abspath(__file__)), "periodic.csv"))
        self.player1_deck = []
        self.player2_deck = []
        self._stack = []
        for pdecks in range(55):
            self.player1_deck.append(game_deck.random())
            self.player2_deck.append(game_deck.random())
        for sdeck in range(8):
            self._stack.append(game_deck.random())



if __name__ == "__main__":
    Game1 = Game(Player("Marie Curie"), Player("Dmitri Mendeleev")) #Create game with our two chemists
    Game1.decks_and_stack() #Print each player's deck and the stack of elements for the game
    Game1.play() #Play the game and print results of each round and the winner of the game
    Game1.stats() #Show addtional stats of the game

    Game1.reset() #Reset the game and to play again with the same players
    Game1.decks_and_stack() #Print each player's deck and the stack of elements for the game
    Game1.play() #Play the game and print results of each round and the winner of the game
    Game1.stats() #Show addtional stats of the game

    Game1.reset() #Reset the game and to play again with the same players
    Game1.decks_and_stack() #Print each player's deck and the stack of elements for the game
    Game1.play() #Play the game and print results of each round and the winner of the game
    Game1.stats() #Show addtional stats of the game

    Game2 = Game(Player("Antoine Lavoisier"), Player("Rosalind Franklin")) #Create game with two new chemists
    Game2.decks_and_stack() #Print each player's deck and the stack of elements for the game
    Game2.play() #Play the game and print results of each round and the winner of the game
    Game2.stats() #Show addtional stats of the game

    Game2.reset() #Reset the game and to play again with the same players
    Game2.decks_and_stack() #Print each player's deck and the stack of elements for the game
    Game2.play() #Play the game and print results of each round and the winner of the game
    Game2.stats() #Show addtional stats of the game

    Game2.reset() #Reset the game and to play again with the same players
    Game2.decks_and_stack() #Print each player's deck and the stack of elements for the game
    Game2.play() #Play the game and print results of each round and the winner of the game
    Game2.stats() #Show addtional stats of the game
