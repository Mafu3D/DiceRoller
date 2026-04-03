import random
from enum import Enum

from pprint import pprint

class Dice():
    """A dice with X sides."""

    def __init__(self, sides: int=6) -> None:
        self.sides = sides

    def get_roll(self) -> int:
        return random.randint(1, self.sides)

class DieCluster():
    """A collection of an amount of die with the same number of sides."""

    def __init__(self, amount: int=1, sides: int=6) -> None:
        self.dice = []
        self.sides = sides
        for _ in range(amount):
            self.dice.append(Dice(self.sides))

    def get_roll(self) -> list[int]:
        return [die.get_roll() for die in self.dice]

    def toDict(self) -> dict:
        return {
            "amount": len(self.dice),
            "sides": self.sides
        }

    def toDiceNotation(self) -> str:
        return f"{len(self.dice)}d{self.sides}"


class Roll():
    """A collection of dice, bonuses, and instructions using dice notation."""

    def __init__(self, dice_notation: str="") -> None:
        parsed_data = ParseDiceNotation.parse(dice_notation)

        self.pos_dice = [DieCluster(amount=die_cluster_data["amount"], sides=die_cluster_data["sides"]) for die_cluster_data in parsed_data.pos_dice]
        self.neg_dice = [DieCluster(amount=die_cluster_data["amount"], sides=die_cluster_data["sides"]) for die_cluster_data in parsed_data.neg_dice]
        self.pos_bonuses = parsed_data.pos_bonuses
        self.neg_bonuses = parsed_data.neg_bonuses

    def roll(self, print_message: bool=False) -> int:
        value = 0
        message = ""

        pos_die_results = []
        for cluster in self.pos_dice:
            values = cluster.get_roll()
            message += f"+{sum(values)} ({cluster.toDiceNotation()}) "
            pos_die_results.extend(cluster.get_roll())

        neg_die_results = []
        for cluster in self.neg_dice:
            values = cluster.get_roll()
            message += f"-{sum(values)} ({cluster.toDiceNotation()}) "
            neg_die_results.extend(cluster.get_roll())

        for pos_value in pos_die_results + self.pos_bonuses:
            value += pos_value

        for neg_value in neg_die_results + self.neg_bonuses:
            value -= neg_value

        if print_message:
            if message.endswith(" "):
                message = message[:-1]
            print(f"{message} + {sum(self.pos_bonuses)} - {sum(self.neg_bonuses)} => {value}")

        return value


    def add_dice(self, dice_notation: str="", amount: int=0, value: int=0):
        raise NotImplementedError

    def remove_dice(self, dice_notation: str="", amount: int=0, value: int=0):
        raise NotImplementedError

    def debug_print(self):
        pprint(self.serializeToDict())

    def serializeToDict(self) -> dict:
        return {
            "pos_dice": [cluster.toDict() for cluster in self.pos_dice],
            "neg_dice": [cluster.toDict() for cluster in self.neg_dice],
            "pos_bonuses": self.pos_bonuses,
            "neg_bonuses": self.neg_bonuses
        }

    def add_bonus(self, toAdd: int|str|list[int|str]):
        raise NotImplementedError
        # if not isinstance(toAdd, list):
        #     toAdd = [toAdd]

        # for value in toAdd:
        #     if isinstance(value, int):
        #         self.bonuses.append(value)
        #     elif isinstance(value, str):
        #         try:
        #             value_int = int(value)
        #             self.bonuses.append(value_int)
        #         except ValueError:
        #             raise ValueError(f"Expected int or str, received {type(value)} instead for {value}")

    def remove_bonus(self, toRemove: int|str|list[int|str]):
        raise NotImplementedError
        # if not isinstance(toRemove, list):
        #     toRemove = [toRemove]

        # toRemove_ints = []
        # for value in toRemove:
        #     if isinstance(value, int):
        #         toRemove_ints.append(value)
        #     elif isinstance(value, str):
        #         try:
        #             value_int = int(value)
        #             toRemove_ints.append(value_int)
        #         except ValueError:
        #             raise ValueError(f"Expected int or str, received {type(value)} instead for {value}")

        # for value in toRemove_ints:
        #     if value in self.bonuses:
        #         self.bonuses.remove(value)

class RollReport():
    pass

class ParsedDiceData():
    def __init__(self) -> None:
        self.pos_dice: list[dict[str, int]] = []
        self.neg_dice: list[dict[str, int]] = []
        self.pos_bonuses: list[int] = []
        self.neg_bonuses: list[int] = []

    def toDict(self) -> dict:
        return {
            "pos_dice": self.pos_dice,
            "neg_dice": self.neg_dice,
            "pos_bonuses": self.pos_bonuses,
            "neg_bonuses": self.neg_bonuses
        }

class ParseDiceNotation():

    @staticmethod
    def parse(dice_notation: str="") -> ParsedDiceData:
        result = ParsedDiceData()

        # Do two passes through the notation to pull out all positive and negative phrases
        neg_phrases = []
        pos_phrases = []
        first_pass = dice_notation.split("+")
        for phrase in first_pass:
            second_pass = phrase.split("-")
            if len(second_pass) > 1:
                neg_phrases.extend(second_pass[1:])
                pos_phrases.append(second_pass[0])
            else:
                pos_phrases.append(phrase)

        # Filter any empty strings
        pos_phrases = list(filter(None, pos_phrases))
        neg_phrases = list(filter(None, neg_phrases))

        for phrase in pos_phrases:
            if "d" in phrase.lower():
                result.pos_dice.append(ParseDiceNotation._parse_dice_phrase(phrase))
            else:
                try:
                    int_value = int(phrase)
                except ValueError:
                    raise ValueError(f"Expected a string value castable to int for {phrase}")
                result.pos_bonuses.append(int_value)

        for phrase in neg_phrases:
            if "d" in phrase.lower():
                result.neg_dice.append(ParseDiceNotation._parse_dice_phrase(phrase))
            else:
                try:
                    int_value = int(phrase)
                except ValueError:
                    raise ValueError(f"Expected a string value castable to int for {phrase}")
                result.neg_bonuses.append(int_value)

        return result

    @staticmethod
    def _parse_dice_phrase(phrase: str) -> dict:
        # Determine amount
        try:
            amount = int(phrase.split("d")[0])
        except ValueError:
            raise ValueError(f"Excepted dice notation: received {phrase}")

        # Determine sides
        try:
            sides = int(phrase.split("d")[-1])
        except ValueError:
            raise ValueError(f"Excepted dice notation: received {phrase}")

        return {
            "sides": sides or 0,
            "amount": amount or 0,
        }