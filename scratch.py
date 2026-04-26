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


def attack_dice(amount, sides, iter=100000, failMethod="all", critMethod="all", critDamageMethod="exploding", debug=False, forceCrit=False, checkAC=False, ac=10):
    """"""
    successes = 0
    total = 0
    crits = 0
    explodes = 0
    for i in range(iter):
        if checkAC:
            toHit = random.randint(1, 10) + random.randint(1, 10)
            if toHit >= ac:
                isHit = True
            else:
                isHit = False

            if debug:
                print(toHit)

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

        if not checkAC:
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

        isCrit = False
        if checkAC and not isHit:
            # Determine if crit
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
            "Crit rate": crits/iter,
            "Average": total/iter
        }


def output_attack_dice(path: str):
    failMethod = "first"
    critMethod = "first"
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

def output_new_attack_dice(path: str, ac=10):
    failMethod = "first"
    critMethod = "first"
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
                             critDamageMethod=critDamageMethod,
                             checkAC=True,
                             ac=ac)
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

def output_dnd_dice(path: str, target):
    output = [
        ["Dice", "Hit Rate", "Crit Rate", "Average"]
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
        result = dnd_dice(int(amount), int(value), target, iter=100000)
        output.append(
            [
                dice,
                result["Hit rate"],
                result["Crit rate"],
                result["Average"],
            ]
        )


    with open(path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(output)

def opposed_rolls(side1=0, side2=0, iter=100000):
    successess = 0
    for i in range(iter):
        a = random.randint(1, 10) + random.randint(1, 10) + side1
        b = random.randint(1, 10) + random.randint(1, 10) + side2
        if a >= b:
            successess += 1

    print(successess/iter)

def dice_pool(amount=2, take=2, target=4, sides=6, bonus=0, iter=10):
    import heapq

    successess = 0
    totalAll = 0
    for i in range(iter):
        values = []
        for _ in range(amount):
            values.append(random.randint(1, sides))
        total = sum(heapq.nlargest(take, values)) + bonus
        if total >= target:
            successess += 1
        totalAll += total

    print(successess/iter)
    # print(totalAll/iter)

def new_dice(first=6, second=4, target=6, bonus=0, iter=10):
    successes = 0
    totalAll = 0
    for i in range(iter):
        value = random.randint(1, first) + random.randint(1, second) + bonus
        if value >= target:
            successes += 1
        totalAll += value

    print(successes/iter)
    # print(totalAll/iter)

def new_dice_opposed(aPrime=6, aWild=6, bPrime=6, bWild=6, aBonus=0, bBonus=0, iter=10):
    successes = 0
    aTotal = 0
    bTotal = 0
    for i in range(iter):
        a = random.randint(1, aPrime) + random.randint(1, aWild) + aBonus
        b = random.randint(1, bPrime) + random.randint(1, bWild) + bBonus
        if a >= b:
            successes += 1


    print(successes/iter)
    # print(totalAll/iter)

if __name__ == "__main__":
    # output_attack_dice(r"C:\Users\matt4\OneDrive\Documents\output.csv")
    # output_dnd_dice(r"C:\Users\matt4\OneDrive\Documents\output.csv", 10)

    # attack_dice(1, 6, 1, "first", "first", "exploding", checkAC=True, ac=10, debug=True)
    # output_new_attack_dice(r"C:\Users\matt4\OneDrive\Documents\output.csv", 15)

    # opposed_rolls(1, 0)
    # opposed_rolls(2, 0)
    # opposed_rolls(3, 0)
    # opposed_rolls(4, 0)
    # opposed_rolls(5, 0)

    # target = 6
    # bonus = 0
    # dice_pool(2, 2, target, 6, bonus, 100000)
    # dice_pool(3, 2, target, 6, bonus, 100000)
    # dice_pool(4, 2, target, 6, bonus, 100000)
    # dice_pool(5, 2, target, 6, bonus, 100000)

    prime = 6
    target = 10
    bonus = 0
    new_dice(prime, 4, target, bonus, 100000)
    new_dice(prime, 6, target, bonus, 100000)
    new_dice(prime, 8, target, bonus, 100000)
    new_dice(prime, 10, target, bonus, 100000)
    new_dice(prime, 12, target, bonus, 100000)

    print("--------")

    b = 8
    new_dice_opposed(6, 4, 6, b, 0, 0, 100000)
    new_dice_opposed(6, 6, 6, b, 0, 0, 100000)
    new_dice_opposed(6, 8, 6, b, 0, 0, 100000)
    new_dice_opposed(6, 10, 6, b, 0, 0, 100000)
    new_dice_opposed(6, 12, 6, b, 0, 0, 100000)


    # dnd_dice(3, 4, 10, 100000)

    # dc1 = DiceCluster(2, 6, [2, 3, -1], True)
    # dc1.roll()
    # print(dc1.get_result())
    # print(dc1.die_results)
    # print(dc1.toString())

    # d = Dice(6)
    # d.roll()
    # print(d.get_result())
    # print(d.toString())

    # dc2 = DiceCluster(3, 4, is_subtractive=True)
    # roll = Roll(dice_clusters=[dc1, dc2])
    # roll.roll(print_message=True)