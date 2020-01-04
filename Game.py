import time
from Colors import *


def game(n, m, players, lands):
    global y
    end = False
    while not end:
        for x in players:
            for i in range(n):
                print()
                for j in range(m):
                    print(lands[i][j].color, CBOLD, lands[i][j].owner, CEND, CGREY, "(", lands[i][j].soldiersCount, ")", CEND, end=" ")
            print()
            if x.number_of_lands() == n * m:
                print(CGREEN, x.name, "you win!", CEND)
                end = True
                break
            if x.number_of_lands() == 0:
                print(CRED2, x.name, "you loose ", CEND)
                players.remove(x)
                continue
            print(x.name, "its your turn !")

            if not x.isAI:
                print("lets increase your troops")
                number_of_xlands = x.number_of_lands()
                while number_of_xlands > 0:
                    la_i = int(input("Enter i: "))
                    la_j = int(input("Enter j: "))
                    if lands[la_i][la_j] in x.landList:
                        print("Enter a number between 1 and", number_of_xlands)
                        increasing_number = int(input())
                        number_of_xlands -= increasing_number
                        lands[la_i][la_j].add_soldier(increasing_number)
                    else:
                        print("its not your land")

                want_attack = input("Enter YES for attack and Enter NO for no attacking: ")
                can_attack = True
                if want_attack == "NO" or want_attack == "no":
                    can_attack = False
                while number_of_xlands < n * m and can_attack:
                    at_i = int(input("Enter i attacker land: "))
                    at_j = int(input("Enter j attacker land: "))
                    print("number of soldiers on this land : ", lands[at_i][at_j].soldiersCount)
                    de_i = int(input("Enter i defender land: "))
                    de_j = int(input("Enter j defender land: "))
                    soldier_used = int(input("Enter number of soldiers you want to use: "))
                    if soldier_used > lands[at_i][at_j].soldiersCount:
                        print("there are not that many troops in this land")
                        continue
                    for y in players:
                        if y.id == lands[de_i][de_j].owner:
                            break
                    lands[at_i][at_j].attack(lands[de_i][de_j], soldier_used, x, y)
                    for i in range(len(x.landList)):
                        if x.landList[i].soldiersCount > 1:
                            can_attack = True
                            break
                        else:
                            can_attack = False
                    want_attack = input("Enter YES for attack and Enter NO for no attacking: ")
                    if want_attack == "NO" or want_attack == "no":
                        can_attack = False

            elif x.isAI:
                x.make_move(lands, n, m)
                # lands_with_least_enemy = []
                # enemy_land_count = 8
                # for land in x.landList:
                #     cnt = 0
                #     for enemy_land in land.adjacencylist:
                #         if enemy_land.owner != land.owner:
                #             cnt += 1
                #     if cnt < enemy_land_count:
                #         enemy_land_count = cnt
                #         lands_with_least_enemy.clear()
                #         lands_with_least_enemy.append(land)
                #     elif cnt == enemy_land_count:
                #         lands_with_least_enemy.append(land)
                #
                # for troops in lands_with_least_enemy:
                #     tmp = int(x.number_of_lands() / len(lands_with_least_enemy))
                #     troops.add_soldier(tmp)
                #     print("troops added in land ", troops.i, troops.j)

                can_attack_ai = True
                dont_attack = False
                while can_attack_ai and not dont_attack:
                    land_with_most_friends_count = 0
                    global defender_land, attacker_land, defender
                    attacker_land = x.landList[0]
                    for land in x.landList:
                        if land.soldiersCount > 1:
                            for enemy_land in land.adjacencylist:
                                if enemy_land.owner != land.owner:
                                    friends = 0
                                    for enemy_land_adj in enemy_land.adjacencylist:
                                        if enemy_land_adj.owner == land.owner:
                                            friends += 1

                                    if friends > land_with_most_friends_count:
                                        land_with_most_friends_count = friends
                                        defender_land = enemy_land
                                        attacker_land = land

                    global defender_player
                    for defender_player in players:
                        try:
                            if defender_player.id == defender_land.owner:
                                break
                        except:
                            dont_attack = True
                            break
                    if attacker_land.soldiersCount - defender_land.soldiersCount > 3:
                        attacker_land.attack(defender_land, attacker_land.soldiersCount, x, defender_player)
                    else:
                        dont_attack = True
                    for i in range(len(x.landList)):
                        if x.landList[i].soldiersCount > 1:
                            can_attack_ai = True
                            break
                        else:
                            can_attack_ai = False



        # time.sleep(0.5)
