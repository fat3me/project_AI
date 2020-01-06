class Player:

    def __init__(self, name, isAI, color, id):
        self.name = name
        self.isAI = isAI
        self.color = color
        self.id = id
        self.soldiers = 0
        self.landList = []

    def add_land(self, land):
        self.landList.append(land)

    def add_soldiers(self):
        self.soldiers += 1

    def get_name(self):
        return self.name

    def number_of_lands(self):
        return len(self.landList)

    def make_move(self, state, n, m, players):
        # evaluation of all nodes
        # self.valuation(n, m, state)

        # DEPLOY
        for i in range(self.number_of_lands()):
            self.valuation(n, m, state, players)
            self.landList.sort(key=lambda x: x.value + x.vulnerability, reverse=True)
            self.landList[0].add_soldier(1)
            # print("adding soldier to ", self.landList[0].i, self.landList[0].j, "with value of: ",
            #       self.landList[0].value, "and vulnerability of:", self.landList[0].vulnerability)

        # ATTACK
        ready_for_attack = []
        for land in self.landList:
            if land.soldiersCount > 1:
                ready_for_attack.append(land)

        for attacker in ready_for_attack:
            enemies = []
            for land in attacker.adjacencylist:
                if not land.owner == attacker.owner:
                    enemies.append(land)
            enemies.sort(key=lambda x: x.soldiersCount, reverse=False)
            if len(enemies) == 0:
                break
            for enemy in enemies:
                if attacker.soldiersCount > enemy.soldiersCount:
                    needed_soldiers = min(enemy.soldiersCount + 3, int(enemy.soldiersCount + enemy.soldiersCount/2) + 1)
                    # if enemy.soldiersCount == 1:
                    #     needed_soldiers = 2
                    if attacker.soldiersCount - needed_soldiers - 1 <= 0:
                        break
                    global enemy_player
                    for p in players:
                        if p.id == enemy.owner:
                            enemy_player = p
                    # print("attacking from:", attacker.i, attacker.j, "  to:", enemy.i, enemy.j, "with", needed_soldiers, "soldiers")
                    # print("------> enemy:", enemy.soldiersCount, "soldiers")
                    attacker.attack(enemy, needed_soldiers, self, enemy_player)
        # self.landList.sort(key=lambda x: x.value, reverse=True)
        # cnt = 0
        # max_val = self.landList[0].value
        # for land in self.landList:
        #     if land.value < max_val:
        #         break
        #     cnt += 1
        # for i in range(cnt):
        #     self.landList[i].add_soldier(int(self.number_of_lands() / cnt))
        #     print("troops added in land ", self.landList[i].i, self.landList[i].j)
        # self.landList[i].add_soldier(int(self.number_of_lands() % cnt))

    def valuation(self, n, m, state, players):
        for i in range(n):
            for j in range(m):
                state[i][j].value = self.evaluate(state[i][j])
                state[i][j].vulnerability = self.vulnerability(state[i][j], players)
                # state[i][j].value = 0
                # state[i][j].value += 8 - len(state[i][j].adjacencylist)
                # friendly_land_cnt = 0
                # enemy_land_cnt = 0
                # friendly_soldier_cnt = 0
                # enemy_soldier_cnt = 0
                # for land in state[i][j].adjacencylist:
                #     if self.id == land.owner:
                #         friendly_land_cnt += 1
                #         friendly_soldier_cnt += land.soldiersCount
                #     else:
                #         enemy_soldier_cnt += land.soldiersCount
                #         enemy_land_cnt += 1
                #
                # if state[i][j].owner == self.id:
                #     state[i][j].value += 1 / state[i][j].soldiersCount
                #     if friendly_land_cnt == 8:
                #         state[i][j].value += -friendly_soldier_cnt
                #     else:
                #         friendly_land_cnt += 1
                #         state[i][j].value += (1 / (
                #                 abs(
                #                     4 - friendly_land_cnt) + 1)) * 10 - friendly_soldier_cnt / friendly_land_cnt + enemy_soldier_cnt / (
                #                                      enemy_land_cnt + 1) - state[i][j].soldiersCount / (
                #                                      enemy_land_cnt + 1)
                # else:
                #     friendly_land_cnt += 1
                #     state[i][
                #         j].value += friendly_land_cnt + friendly_soldier_cnt / friendly_land_cnt - enemy_soldier_cnt / (
                #             enemy_land_cnt + 1)
                #     state[i][j].value -= state[i][j].soldiersCount / 5

    def evaluate(self, land):
        total_adjacent_lands = 0
        friendly_adjacent_lands = 0
        enemy_adjacent_lands = 0
        friendly_adjacent_stocked_lands = 0
        enemy_adjacent_stocked_lands = 0

        is_enemy = False
        enemy_id = 0
        # this could be changed to max amount of friendlies stocked ( i should check to see witch will do better)
        total_adjacent_friendly_stocked_soldiers = 0
        total_adjacent_enemy_stocked_soldiers = 0
        if not self.id == land.owner:
            is_enemy = True

        for l in land.adjacencylist:
            if l.owner == self.id:
                friendly_adjacent_lands += 1
                # checking if soldiers in this adjacent land are stocked here
                if not is_enemy:
                    is_stocked = True
                    for l2 in l.adjacencylist:
                        if not l2.owner == self.id:
                            is_stocked = False
                            break
                    if is_stocked:
                        # print("land", l.i, l.j, " is stocked between friendlies with ", l2.soldiersCount,
                        #       " extra soldiers")
                        friendly_adjacent_stocked_lands += 1
                        total_adjacent_friendly_stocked_soldiers += l2.soldiersCount - 1
            else:
                enemy_adjacent_lands += 1
                if is_enemy:
                    is_stocked = True
                    for l2 in l.adjacencylist:
                        if l2.owner == self.id:
                            is_stocked = False
                            break
                    if is_stocked:
                        # print("land", l.i, l.j, " is stocked between friendlies with ", l2.soldiersCount,
                        #       " extra soldiers")
                        enemy_adjacent_stocked_lands += 1
                        total_adjacent_enemy_stocked_soldiers += l2.soldiersCount - 1

            total_adjacent_lands += 1

        stocked_soldiers_value = 0
        if not is_enemy:
            if friendly_adjacent_stocked_lands > 0:
                stocked_soldiers_value = total_adjacent_friendly_stocked_soldiers / friendly_adjacent_stocked_lands

            value = 1 / (abs(
                friendly_adjacent_lands - enemy_adjacent_lands) + 1) + 1 / 10 * land.soldiersCount - stocked_soldiers_value
            if friendly_adjacent_lands == len(land.adjacencylist):
                value = -100
        else:
            if enemy_adjacent_stocked_lands > 0:
                stocked_soldiers_value = total_adjacent_enemy_stocked_soldiers / enemy_adjacent_stocked_lands

            value = 1 / (abs(
                friendly_adjacent_lands / total_adjacent_lands - enemy_adjacent_lands) + 1) + 1 / land.soldiersCount - stocked_soldiers_value
        return value

    def vulnerability(self, land, players):
        enemy_soldiers = 0
        global player
        if land.owner == self.id:
            for l in land.adjacencylist:
                if not l.owner == self.id:
                    if l.soldiersCount > enemy_soldiers:
                        enemy_soldiers = l.soldiersCount - 1
                        for p in players:
                            if p.id == l.owner:
                                # print("shiiiiiiiiiiiiiiiiiiiiiiit")
                                player = p

            # print("max enemies around", land.i, land.j,"with",land.soldiersCount,"soldiers", " was ", enemy_soldiers, "witch belonged to:", player.id)
            return (20 * enemy_soldiers + len(player.landList)) / (20 * land.soldiersCount)
        else:
            for l in land.adjacencylist:
                if not l.owner == land.owner:
                    if l.soldiersCount > enemy_soldiers:
                        enemy_soldiers = l.soldiersCount
                        for p in players:
                            if p.id == l.owner:
                                player = p
            return 1


def utility(self, current_state, n, m):
    res = 0
    for i in range(n):
        for j in range(m):
            if current_state[i][i].owner == self.id:
                res += current_state[i][i].value
