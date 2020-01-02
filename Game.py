def game(n, m, players, lands):
    global y
    end = False
    while not end:
        for x in players:
            for i in range(n):
                print()
                for j in range(m):
                    print(lands[i][j].owner, end=" ")
            print()
            print(x.name, "its your turn !")
            if x.number_of_lands() == 0:
                print(x.name, "you loose ")
                players.remove(x)
                continue

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
                if want_attack == "YES":
                    can_attack = True
                    while number_of_xlands < n * m and can_attack:
                        at_i = int(input("Enter i attacker land: "))
                        at_j = int(input("Enter j attacker land: "))
                        de_i = int(input("Enter i defender land: "))
                        de_j = int(input("Enter j defender land: "))
                        soldier_used = int(input("Enter number of soldiers: "))
                        if soldier_used > lands[at_i][at_j].soldiersCount:
                            print("there are not that many troops in this land")
                            continue
                        for y in players:
                            if y.id == lands[de_i][de_j].owner:
                                break
                        lands[at_i][at_j].attack(lands[de_i][de_j], soldier_used, x, y)
                        for i in range(len(x.landList)):
                            if x.landList[i].soldiersCount != 1:
                                can_attack = True
                                break
                            else:
                                can_attack = False
                        want_attack = input("Enter YES for attack and Enter NO for no attacking: ")
                        if want_attack == "NO":
                            can_attack = False

            elif x.isAI:
                lands_with_least_enemy = []
                enemy_land_count = 8
                for land in x.landList:
                    cnt = 0
                    for enemy_land in land.adjacencylist:
                        if enemy_land.owner != land.owner:
                            cnt += 1
                    if cnt < enemy_land_count:
                        enemy_land_count = cnt
                        lands_with_least_enemy.clear()
                        lands_with_least_enemy.append(land)
                    elif cnt == enemy_land_count:
                        lands_with_least_enemy.append(land)

                for troops in lands_with_least_enemy:
                    tmp = int(x.number_of_lands() / len(lands_with_least_enemy))
                    troops.add_soldier(tmp)
                    print("troops add in land ", troops.i, troops.j)

                can_attack_ai = True
                while can_attack_ai:
                    land_with_most_friends_count = 0
                    global defender_land, attacker_land, defender
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
                                        can_attack_ai = True
                        else:
                            can_attack_ai = False
                    global defender_player
                    for defender_player in players:
                        if defender_player.id == defender_land.owner:
                            break
                    if attacker_land.soldiersCount - defender_land.soldiersCount > 3:
                        attacker_land.attack(defender_land, attacker_land.soldiersCount, x, defender_player)



            if x.number_of_lands() == n * m:
                end = True