from Move import Move
from Node import Node
import copy


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

    def a_star_deploy(self, game_map, n, m):
        available_soldiers = self.number_of_lands()

    # def a_star_attack(self, players):
    #     for land in self.landList:
    #         if land.soldiersCount>1:

    # def find_best_option(self, player, land, given_soldiers):
    #     route = []
    #     for i in range (2, land.soldiersCount-1):
    #

    def minimax(self, node, main_player, depth):
        if depth == 10:
            return node.value
        if node.isTerminal:
            return node.value

        if node.player.id is main_player.id:
            value = int('-inf')

    def min_max(self, players, cnt, node, n, m):
        if cnt == 5 * len(players):
            return node.value
        if node.isTerminal:
            return node.value

        ready_for_attack = []
        for land in node.player.landList:
            if land.soldiersCount > 1:
                ready_for_attack.append(land)

        # avalibale_lands_for_attack = len(ready_for_attack)
        is_attack_possible = True
        while len(ready_for_attack) > 0 and is_attack_possible:
            is_attack_possible = False
            for attacker in ready_for_attack:
                moves = []
                enemies = []
                for land in attacker.adjacencylist:
                    if not land.owner == attacker.owner:
                        enemies.append(land)
                enemies.sort(key=lambda x: x.soldiersCount, reverse=False)
                if len(enemies) == 0:
                    break
                enemy_cnt = len(enemies)
                for enemy in enemies:
                    if attacker.soldiersCount > enemy.soldiersCount:
                        needed_soldiers = min(enemy.soldiersCount + 3,
                                              int(enemy.soldiersCount + enemy.soldiersCount / 2) + 1)
                        if enemy.soldiersCount == 1:
                            if attacker.soldiersCount >= 3:
                                needed_soldiers = 3
                        if attacker.soldiersCount - needed_soldiers - 1 <= 0:
                            break
                        is_attack_possible = True
                        global enemy_player
                        for p in players:
                            if p.id == enemy.owner:
                                enemy_player = p
                        # print("attacking from:", attacker.i, attacker.j, "  to:", enemy.i, enemy.j, "with", needed_soldiers,
                        #       "soldiers")
                        # print("------> enemy:", enemy.soldiersCount, "soldiers")
                        for i in range(needed_soldiers, attacker.soldiersCount):
                            attacker_cp = copy.deepcopy(attacker)
                            enemy_cp = copy.deepcopy(enemy)
                            player_cp = copy.deepcopy(node.player)
                            enemy_player_cp = copy.deepcopy(enemy_player)
                            moves.append(Move(attacker_cp, enemy_cp, i))
                            attacker_cp.attack(enemy, i, node.player, enemy_player_cp)
                            # if success:
                            #     enemy_cnt -= 1
                            # players[(players.index(player) + 1) % len(players)]
                            # if node.player.id == self.id:
                            #     value = self.utility(node.player, n, m)
                            # else:
                            #     value = self.utility(players)
                            value = node.calculate_utility(n, m)
                            next_node = Node(node.main_player, node.next_player,
                                             players[(players.index(node.next_player) + 1) % len(players)], moves,
                                             value, node, len(node.player.landList) == m * n)
            ready_for_attack = []
            for land in node.player.landList:
                if land.soldiersCount > 1:
                    ready_for_attack.append(land)

    def make_move(self, state, n, m, current_player, players, turn):
        # evaluation of all nodes
        # DEPLOY
        if turn != 1:
            for i in range(self.number_of_lands()):
                current_player.valuation(n, m, state, players)
                current_player.landList.sort(key=lambda x: x.value + x.vulnerability, reverse=True)
                current_player.landList[0].add_soldier(1)
                # print("adding soldier to ", current_player.landList[0].i, current_player.landList[0].j, "with value of: ",
                #       current_player.landList[0].value, "and vulnerability of:", current_player.landList[0].vulnerability)
        # if is_first_turn:
        #     return
        # ATTACK
        if turn != 0:
            ready_for_attack = []
            for land in current_player.landList:
                if land.soldiersCount > 1:
                    ready_for_attack.append(land)
            is_attack_possible = True
            while len(ready_for_attack) > 0 and is_attack_possible:
                is_attack_possible = False
                for attacker in ready_for_attack:
                    enemies = []
                    for land in attacker.adjacencylist:
                        if not land.owner == attacker.owner:
                            enemies.append(land)
                    enemies.sort(key=lambda x: x.soldiersCount, reverse=False)
                    if len(enemies) == 0:
                        break
                    enemy_cnt = len(enemies)
                    for enemy in enemies:
                        if attacker.soldiersCount > enemy.soldiersCount:
                            needed_soldiers = min(enemy.soldiersCount + 3,
                                                  int(enemy.soldiersCount + enemy.soldiersCount / 2) + 1)
                            if enemy.soldiersCount == 1:
                                needed_soldiers = 2
                            global enemy_player
                            for p in players:
                                if p.id == enemy.owner:
                                    enemy_player = p
                            if attacker.soldiersCount - needed_soldiers - 1 <= 0:
                                total_soldiers = 0
                                for land in enemy.adjacencylist:
                                    if land.owner == attacker.owner:
                                        total_soldiers += land.soldiersCount - 1
                                if total_soldiers > enemy.soldiersCount + 2:
                                    is_attack_possible = True
                                    attacker.attack(enemy, attacker.soldiersCount - 1, current_player, enemy_player)
                                break
                            is_attack_possible = True
                            if enemy_cnt == 1:
                                needed_soldiers = attacker.soldiersCount - 1

                            print("attacking from:", attacker.i, attacker.j, "  to:", enemy.i, enemy.j, "with", needed_soldiers,
                                  "soldiers")
                            print("------> enemy:", enemy.soldiersCount, "soldiers")
                            res = attacker.attack(enemy, needed_soldiers, current_player, enemy_player)
                            if res:
                                enemy_cnt -= 1
                            elif attacker.soldiersCount - 1 > enemy.soldiersCount:
                                res = attacker.attack(enemy, attacker.soldiersCount - 1, current_player, enemy_player)
                                if res:
                                    enemy_cnt -= 1
                        else:
                            total_soldiers = 0
                            for land in enemy.adjacencylist:
                                if land.owner == attacker.owner:
                                    total_soldiers += land.soldiersCount - 1
                            global enemy_player2
                            for p in players:
                                if p.id == enemy.owner:
                                    enemy_player2 = p
                            if total_soldiers > enemy.soldiersCount + 2:
                                is_attack_possible = True
                                attacker.attack(enemy, attacker.soldiersCount - 1, current_player, enemy_player2)

                ready_for_attack = []
                for land in current_player.landList:
                    if land.soldiersCount > 1:
                        ready_for_attack.append(land)

            # current_player.landList.sort(key=lambda x: x.value, reverse=True)
            # cnt = 0
            # max_val = current_player.landList[0].value
            # for land in current_player.landList:
            #     if land.value < max_val:
            #         break
            #     cnt += 1
            # for i in range(cnt):
            #     current_player.landList[i].add_soldier(int(current_player.number_of_lands() / cnt))
            #     print("troops added in land ", current_player.landList[i].i, current_player.landList[i].j)
            # current_player.landList[i].add_soldier(int(current_player.number_of_lands() % cnt))



    def valuation(self, n, m, state, players):
        for i in range(n):
            for j in range(m):
                if state[i][j].owner == self.id:
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
        value = land.value
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
                # if not is_enemy:
                #     is_stocked = True
                #     for l2 in l.adjacencylist:
                #         if not l2.owner == self.id:
                #             is_stocked = False
                #             break
                #     if is_stocked:
                #         print("land", l.i, l.j, " is stocked between friendlies with ", l.soldiersCount - 1,
                #               " extra soldiers")
                #         friendly_adjacent_stocked_lands += 1
                #         total_adjacent_friendly_stocked_soldiers += l.soldiersCount - 1
                #         break
            else:
                enemy_adjacent_lands += 1
                # if is_enemy:
                #     is_stocked = True
                #     for l2 in l.adjacencylist:
                #         if l2.owner == self.id:
                #             is_stocked = False
                #             break
                #     if is_stocked:
                #         print("enemy land", l.i, l.j, " is stocked between friendlies with ", l.soldiersCount,
                #               " extra soldiers")
                #         enemy_adjacent_stocked_lands += 1
                #         total_adjacent_enemy_stocked_soldiers += l.soldiersCount - 1

            total_adjacent_lands += 1

        stocked_soldiers_value = 0
        if not is_enemy:
            if friendly_adjacent_stocked_lands > 0:
                stocked_soldiers_value = total_adjacent_friendly_stocked_soldiers / friendly_adjacent_stocked_lands

            value = 1 / (abs(friendly_adjacent_lands - enemy_adjacent_lands) + 1) + 1 / (
                    10 * land.soldiersCount) - stocked_soldiers_value

            if friendly_adjacent_lands == len(land.adjacencylist):
                value = 0

        # else:
        #     if enemy_adjacent_stocked_lands > 0:
        #         stocked_soldiers_value = total_adjacent_enemy_stocked_soldiers / enemy_adjacent_stocked_lands
        #
        #     value = 1 / (abs(
        #         friendly_adjacent_lands / total_adjacent_lands - enemy_adjacent_lands) + 1) + 1 / land.soldiersCount - stocked_soldiers_value
        return value

    def vulnerability(self, land, players):
        enemy_soldiers = 0
        player = self
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
            if player == self:
                return 0
            return (20 * enemy_soldiers + len(player.landList)) / (20 * land.soldiersCount)
        # else:
        #     for l in land.adjacencylist:
        #         if not l.owner == land.owner:
        #             if l.soldiersCount > enemy_soldiers:
        #                 enemy_soldiers = l.soldiersCount
        #                 for p in players:
        #                     if p.id == l.owner:
        #                         player = p
        #     return 1

    def utility(self, player, n, m):

        res = 0
        for land in player.landList:
            res += land.value * land.soldiersCount
        return res / (n * m - len(player.landList) + 0.00001)
