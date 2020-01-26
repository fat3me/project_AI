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
        self.vulnerability = 0

    def add_soldier(self, num):
        self.soldiersCount += num

    def set_color(self, color):
        self.color = color

    def set_id(self, idOwner):
        self.owner = idOwner

    def attack(self, defender, soldiers_used, attacking_player, defender_player):
        if self.adjacencylist.__contains__(defender):

            while self.soldiersCount > 1 and defender.soldiersCount > 0 and soldiers_used > 0:
                attacker_dice = int(random.randint(1, 6))
                print("attacker_dice : ", attacker_dice)
                defender_dice = int(random.randint(1, 6))
                print("defender dice : ", defender_dice)
                if attacker_dice > defender_dice:
                    defender.soldiersCount -= 1
                    defender_player.soldiers -= 1
                elif attacker_dice == defender_dice:
                    print("dices were equal, ROLL AGAIN!!")
                else:
                    self.soldiersCount -= 1
                    attacking_player.soldiers -= 1
                    soldiers_used -= 1

            if defender.soldiersCount == 0:
                print("player", self.owner, " attacking from: ", self.i, self.j, "captured land", defender.i,
                      defender.j, "from player", defender.owner)
                defender_player.landList.remove(defender)
                defender.owner = self.owner
                defender.color = self.color
                defender.soldiersCount = soldiers_used
                self.soldiersCount = self.soldiersCount - soldiers_used
                attacking_player.landList.append(defender)
                return True
            else:
                print("Oops player", self.owner, " couldn't capture the land from player", defender.owner)
                return False
        else:
            print("you can NOT attack land in: ", defender.i, defender.j, " from: ", self.i, self.j, "!! ")
            return False

