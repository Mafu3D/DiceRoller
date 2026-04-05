from lib import *
import random
import csv

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

def test_crits_2(target = 15, threshold = 0, iter:int=1000):

    successes = 0
    for i in range(iter):
        roll1 = Roll("1d10")
        value1 = roll1.roll()

        roll2 = Roll("1d10")
        value2 = roll2.roll()

        if abs(value1-value2) <= threshold and (value1 + value2) > target:
            successes += 1

    print(successes / iter)

def test_crits_3(amount, sides, iter=100000):
    """"""
    successes = 0
    total = 0
    for i in range(iter):
        values = []
        isHit = True
        for _ in range(amount):
            values.append(random.randint(1, sides))

        if all(x == 1 for x in values):
            isHit = False

        if isHit:
            total += sum(values)
            successes += 1

        # print(values)
        # print(isHit)

    print(f"Success rate:    {successes/iter}")
    print(f"Average result:  {total/iter}")


def attack_dice(amount, sides, iter=100000, failMethod="all", critMethod="all", critDamageMethod="exploding", debug=False, forceCrit=False):
    """"""
    successes = 0
    total = 0
    crits = 0
    explodes = 0
    for i in range(iter):
        values = []
        for _ in range(amount):
            values.append(random.randint(1, sides))

        if forceCrit:
            if critMethod=="all":
                values = [sides for i in range(amount)]
            elif critMethod=="first":
                values[0] = sides

        if debug:
            print(f"Initial roll: {values}")

        # Determine if fail
        isHit = True
        if failMethod == "all":
            if all(x == 1 for x in values):
                isHit = False
        elif failMethod == "first":
            if values[0] == 1:
                isHit = False

        if not isHit and debug:
            print("Roll failed")

        # Determine if crit
        isCrit = False
        if critMethod == "all":
            if all(x == sides for x in values):
                isCrit = True
        elif critMethod == "first":
            if values[0] == sides:
                isCrit = True

        if isCrit and debug:
            print("Crit!")

        # Determine crit damage
        critValues = []
        if isCrit:
            crits += 1
            if critDamageMethod == "exploding":
                critValue = sides
                while critValue == sides:
                    critValue = random.randint(1, sides)
                    critValues.append(critValue)
                    explodes += 1
            elif critDamageMethod == "once":
                pass
            elif critDamageMethod == "max":
                pass

            if debug:
                print(f"Crit damage: {critValues}")

        values.extend(critValues)

        if isHit:
            total += sum(values)
            if debug:
                print(f"Total: {total}")
            successes += 1

        # print(values)
        # print(isHit)

    return {
        "Hit rate": successes/iter,
        "Crit rate": crits/iter,
        "Explode rate": explodes/iter,
        "Average": total/iter
    }

def dnd_dice(amount, sides, ac=10, iter=100000, debug=False, forceCrit=False):
    """"""
    successes = 0
    total = 0
    crits = 0
    for i in range(iter):
        value = random.randint(1, 20)

        if forceCrit:
            value = 20

        if debug:
            print(f"Initial roll: {value}")

        # Determine if fail
        isHit = True
        if value < ac:
            isHit = False

        if not isHit and debug:
            print("Roll failed")

        # Determine if crit
        isCrit = False
        if value == 20:
            isCrit = True
            crits += 1

        if isCrit and debug:
            print("Crit!")

        # Determine damage
        damageValues = []
        for i in range(amount):
            damageValues.append(random.randint(1, sides))

        critValues = []
        if isCrit:
            for i in range(amount):
                critValues.append(random.randint(1, sides))

        damageValues.extend(critValues)

        if isHit:
            total += sum(damageValues)
            if debug:
                print(f"Total: {total}")
            successes += 1

        # print(values)
        # print(isHit)

    return {
            "Hit rate": successes/iter,
            "Crit rate": {crits/iter},
            "Average": {total/iter}
        }


def run(path: str):
    failMethod = "all"
    critMethod = "all"
    critDamageMethod = "exploding"

    output = [
        ["Dice", "Hit Rate", "Crit Rate", "Average", "Explode Rate",]
    ]

    dice_to_test = [
        "1d4",
        "1d6",
        "1d8",
        "1d10",
        "1d12",
        "2d4",
        "2d6",
        "2d8",
        "2d10",
        "3d4",
        "3d6"
    ]

    for dice in dice_to_test:
        amount, value = dice.split("d")
        result = attack_dice(int(amount), int(value), iter=100000,
                             failMethod=failMethod,
                             critMethod=critMethod,
                             critDamageMethod=critDamageMethod)
        output.append(
            [
                dice,
                result["Hit rate"],
                result["Crit rate"],
                result["Average"],
                result["Explode rate"],
            ]
        )


    with open(path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(output)


if __name__ == "__main__":
    run(r"C:\Users\matt4\OneDrive\Documents\output.csv")

    # dnd_dice(3, 4, 10, 100000)