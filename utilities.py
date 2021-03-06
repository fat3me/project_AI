import random


def filling_matrix(n, m, numberOfPlayers, players, lands):
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
                p.landList.append(lands[i][j])
                land_num -= 1


def filling_adjacency_lists(n, m, lands):
    for i in range(n):
        for j in range(m):
            if j-1 >= 0:
                lands[i][j].adjacencylist.append(lands[i][j - 1])
            if j+1 < m:
                lands[i][j].adjacencylist.append(lands[i][j + 1])
            if i+1< n:
                lands[i][j].adjacencylist.append(lands[i + 1][j])
            if i-1 >= 0:
                lands[i][j].adjacencylist.append(lands[i - 1][j])
            if i+1< n and j-1 >= 0:
                lands[i][j].adjacencylist.append(lands[i + 1][j - 1])
            if i + 1 < n and j + 1 < m:
                lands[i][j].adjacencylist.append(lands[i + 1][j + 1])
            if i-1 >= 0 and j + 1 < m:
                lands[i][j].adjacencylist.append(lands[i - 1][j + 1])
            if i - 1 >= 0 and j-1 >= 0:
                lands[i][j].adjacencylist.append(lands[i - 1][j - 1])

