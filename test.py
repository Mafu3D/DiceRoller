from lib import *

"""
Dice Notation:
    <amount>d<value>
    Ex. 2d6 = two six sided die

    2d6kh or 2d6kh1 => two six sided die, take the highest
    4d6kh2 => four six sided die, take the highest 2
    4d6kh1kl1 -=> four six sided die, take the highest and lowest
"""

def test_crits(die: str, threshold: int=20, iter: int=1000):
    successes = 0
    for i in range(iter):
        roll = Roll(die)
        value = roll.roll()
        if value >= threshold:
            successes += 1

    print(successes / iter)

def test_crits_2(threshold = 15, iter:int=1000):

    successes = 0
    for i in range(iter):
        roll1 = Roll("1d10")
        value1 = roll1.roll()

        roll2 = Roll("1d10")
        value2 = roll2.roll()

        if value1 == value2 and (value1 + value2) > threshold:
            successes += 1

    print(successes / iter)

if __name__ == "__main__":
    # simple = "2d10+3"
    # complex = "1d8+3+2d6-1d4"
    # super_complex = "2d6a+9-5"

    # roll = Roll(complex)
    # # roll.debug_print()
    # roll.roll(print_message=True)

    test_crits("2d10", 16, 100000)
    # test_crits_2(10, 100000)