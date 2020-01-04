from Land import Land
from Player import Player
import random
from Game import game
from utilities import filling_matrix, filling_adjacency_lists
from Colors import *


if __name__ == '__main__':

    f = open("inputs.txt", "r")
    artificialPlayerCount = int(f.readline())
    physicalPlayerCount = int(f.readline())
    numberOfPlayers = int(artificialPlayerCount + physicalPlayerCount)
    n = int(f.readline())
    m = int(f.readline())

    colors = [CRED, CGREEN, CYELLOW, CBLUE, CVIOLET, CBEIGE]
    random.shuffle(colors)
    players = []
    lands = [[Land(i, j) for j in range(n)] for i in range(m)]
    i = 0
    for i in range(physicalPlayerCount):
        players.append(Player(input("player " + str(i) + " please enter your name: "), False, colors[i], i))

    for j in range(artificialPlayerCount):
        players.append(Player("player " + str(j + i + 1), True, colors[j + i + 1], j + i + 1))

    random.shuffle(players)

    for i in range(n):
        for j in range(m):
            lands[i][j] = Land(i, j)

    filling_matrix(n, m, numberOfPlayers, players, lands)
    filling_adjacency_lists(n, m, lands)
    game(n, m, players, lands)

    print('\x1b[6;30;42m' + 'Success!' + '\x1b[0m')



















