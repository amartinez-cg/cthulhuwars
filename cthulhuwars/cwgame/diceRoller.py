import random


class DiceRoller:

    def __init__(self, num_dice=2, num_sides=6):
        self.num_dice = num_dice
        self.num_sides = num_sides

    def __roll(self):
        result = random.randint(1, self.num_sides)
        return result

    def roll_dice(self):
        dice_results = []
        for _ in range(self.num_dice):
            dice_results.append(int(self.__roll()))
        return dice_results

    def interpret_dice(self):
        results = {'kill': 0,
                   'pain': 0
                   }

        dice_results = self.roll_dice()

        for roll in dice_results:
            if roll == 4 or roll == 5:
                results['pain'] += 1
            elif roll == 6:
                results['kill'] += 1

        return results

def roll_combat_dice(nDice):
    dice = DiceRoller(num_dice=nDice, num_sides=6)
    result = dice.interpret_dice()
    return result

