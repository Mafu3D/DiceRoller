import random
from enum import Enum

from pprint import pprint

class Dice():
    """A dice with X sides."""

    def __init__(self, sides: int=6) -> None:
        self.sides = sides
        self.has_rolled = False
        self.result = None

    def roll(self) -> int:
        self.has_rolled = True
        self.result = random.randint(1, self.sides)
        return self.result

    def get_result(self) -> int:
        return self.result

    def toString(self) -> str:
        return f"d{self.sides}"

class DiceCluster():
    """A collection of an amount of die with the same number of sides."""

    def __init__(self, amount: int=1, sides: int=6, bonuses=[], is_subtractive: bool=False) -> None:
        self.sides = sides
        self.is_subtractive = is_subtractive
        self.bonuses = bonuses

        self.die_results = []
        self.dice = []
        self.has_rolled = False
        self.roll_report = RollReport()
        self.result = 0
        for _ in range(amount):
            self.dice.append(Dice(self.sides))

    @property
    def modifier(self) -> int:
        return -1 if self.is_subtractive else 1

    def roll(self) -> list[int]:
        for die in self.dice:
            die_result = die.roll() * self.modifier
            self.die_results.append(die_result)
            self.roll_report.add_dice(die, die_result)

        for bonus in self.bonuses:
            self.roll_report.add_bonuses(bonus)

        self.result = sum(self.die_results) + sum(self.bonuses)

        self.roll_report.total = self.result
        self.has_rolled = True
        return self.result

    def get_result(self) -> list[int]:
        return self.result

    def toString(self) -> str:
        bonus_string = ""
        for bonus in self.bonuses:
            bonus_string += f"{'+' if bonus >= 0 else ''}{str(bonus)}"
        return f"{'+' if not self.is_subtractive else '-'}{len(self.dice)}d{self.sides}{bonus_string}"


class Roll():
    """A collection of dice, bonuses, and instructions using dice notation."""

    def __init__(self, dice_clusters: list[DiceCluster]|DiceCluster=[], bonuses: list[int]=[], dice_notation: str="") -> None:
        # parsed_data = ParseDiceNotation.parse(dice_notation)

        # self.dice_clusters = [DiceCluster(amount=die_cluster_data["amount"], sides=die_cluster_data["sides"]) for die_cluster_data in parsed_data.pos_dice]
        if not isinstance(dice_clusters, list):
            dice_clusters = [dice_clusters]
        self.dice_clusters = dice_clusters
        self.bonuses = bonuses

    def roll(self, print_message: bool=False) -> int:
        total = 0
        message = ""

        dice_results = []
        for cluster in self.dice_clusters:
            cluster.roll()
            values = cluster.get_results()
            dice_results.extend(values)

        for total in dice_results + self.bonuses:
            total += total



        return total


    def add_dice(self, dice_notation: str="", amount: int=0, value: int=0):
        raise NotImplementedError

    def remove_dice(self, dice_notation: str="", amount: int=0, value: int=0):
        raise NotImplementedError

    def debug_print(self):
        pprint(self.serializeToDict())

    def serializeToDict(self) -> dict:
        return {
            "pos_dice": [cluster.toDict() for cluster in self.dice_clusters],
            "neg_dice": [cluster.toDict() for cluster in self.neg_dice],
            "pos_bonuses": self.bonuses,
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

    def __init__(self):
        self.dice_results = {}
        self.bonuses = []
        self.is_subtractive = False
        self.total = None

    def add_dice(self, die: Dice, result: int):
        self.dice_results[die.toString()] = result

    def set_is_subtractive(self, value: bool):
        self.is_subtractive = value

    def add_bonuses(self, bonus: int):
        self.bonuses.append(bonus)

    def set_total(self, total: int):
        self.total = total

    def get_message(self) -> str:
        output = ""
        modifier = "-" if self.is_subtractive else "+"
        output += f"{modifier}"
        for dice, result in self.dice_results:
            output += f"{result} ({dice})"
        return output

class RollFactory():
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