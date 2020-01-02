import random


class Land:
    def __init__(self, i: int, j: int):
        self.i = i
        self.j = j
        self.color = "white"
        self.owner = -1
        self.adjacencylist = []
        self.soldiersCount = 1

    def add_soldier(self):
        self.soldiersCount += 1

    def set_color(self, color):
        self.color = color

    def set_id(self, idOwner):
        self.owner = idOwner

    def attack(self, defender):
        if self.adjacencylist.__contains__(defender):
            while self.soldiersCount > 1 and defender.soldiersCount > 0:
                attacker_dice = int(random.randint(1, 6))
                print("attacker_dice : ", attacker_dice)
                defender_dice = int(random.randint(1, 6))
                print("defender dice : ", defender_dice)
                if attacker_dice > defender_dice:
                    defender.soldiersCount -= 1
                else:
                    self.soldiersCount -= 1
        else:
            print("you can NOT attack this land !! ")

        if defender.soldiersCount == 0:
            print("player", self.owner, "captured land from player", defender.owner)
            defender.owner = self.owner
            defender.color = self.color
            defender.soldiersCount = self.soldiersCount - 1
            self.soldiersCount = 1
        else:
            print("Oops player", self.owner, " couldn't capture the land from player", defender.owner)




