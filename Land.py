import random


class Land:
    def __init__(self, i: int, j: int):
        self.i = i
        self.j = j
        self.color = "white"
        self.owner = -1
        self.adjacencylist = []
        self.soldiersCount = 1
        self.value = 0

    def add_soldier(self, num):
        self.soldiersCount += num

    def set_color(self, color):
        self.color = color

    def set_id(self, idOwner):
        self.owner = idOwner

    def attack(self, defender, soldiers_used, attacking_player, defender_player):
        if self.adjacencylist.__contains__(defender):

            while soldiers_used > 1 and defender.soldiersCount > 0:
                attacker_dice = int(random.randint(1, 6))
                print("attacker_dice : ", attacker_dice)
                defender_dice = int(random.randint(1, 6))
                print("defender dice : ", defender_dice)
                if attacker_dice > defender_dice:
                    defender.soldiersCount -= 1
                    defender_player.soldiers -= 1
                else:
                    self.soldiersCount -= 1
                    attacking_player.soldiers -= 1
                    soldiers_used -= 1
        else:
            print("you can NOT attack this land !! ")

        if defender.soldiersCount == 0:
            print("player", self.owner, "captured land", defender.i, defender.j, "from player", defender.owner)
            defender_player.landList.remove(defender)
            defender.owner = self.owner
            defender.color = self.color
            defender.soldiersCount = soldiers_used - 1
            self.soldiersCount = 1
            attacking_player.landList.append(defender)

        else:
            print("Oops player", self.owner, " couldn't capture the land from player", defender.owner)




