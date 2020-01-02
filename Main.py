from Player import Player
from Land import Land
import random


def filling_matrix():
    more_land = (n * m) % numberOfPlayers
    for p in players:
        land_num = (n * m) // numberOfPlayers
        if more_land > 0:
            land_num += 1
            more_land -= 1
        while land_num > 0:
            i = random.randrange(0, n)
            j = random.randrange(0, m)
            if lands[i][j].owner == -1:
                lands[i][j].set_id(p.id)
                lands[i][j].set_color(p.color)
                land_num -= 1


if __name__ == '__main__':

    artificialPlayerCount = int(input("please enter artificial player count: "))
    physicalPlayerCount = int(input("please enter physical player count: "))
    numberOfPlayers = int(artificialPlayerCount + physicalPlayerCount)
    n = int(input("enter n: "))
    m = int(input("enter m: "))

    colors = ["red", "blue", "yellow", "green", "pink", "orange", "white"]
    random.shuffle(colors)
    players = []
    lands = [[Land(i, j) for j in range(n)] for i in range(m)]

    for i in range(numberOfPlayers):
        players.append(Player(input("player " + str(i) + " please enter your name: "), True, colors[i], i))

    random.shuffle(players)

    for i in range(n):
        for j in range(m):
            lands[i][j] = Land(i, j)

    filling_matrix()

    for i in range(n):
        for j in range(m):
            try:
                lands[i][j].adjacencylist.append(lands[i][j - 1])
            except:
                pass
            try:
                lands[i][j].adjacencylist.append(lands[i][j + 1])
            except:
                pass
            try:
                lands[i][j].adjacencylist.append(lands[i + 1][j])
            except:
                pass
            try:
                lands[i][j].adjacencylist.append(lands[i - 1][j])
            except:
                pass
            try:
                lands[i][j].adjacencylist.append(lands[i + 1][j - 1])
            except:
                pass
            try:
                lands[i][j].adjacencylist.append(lands[i + 1][j + 1])
            except:
                pass
            try:
                lands[i][j].adjacencylist.append(lands[i - 1][j + 1])
            except:
                pass
            try:
                lands[i][j].adjacencylist.append(lands[i - 1][j - 1])
            except:
                continue

    lands[1][1].soldiersCount += 5
    lands[1][1].attack(lands[0][0])



















