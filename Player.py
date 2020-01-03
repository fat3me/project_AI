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

    def make_move(self, state, n, m):
        # evaluation of all nodes
        self.valuation(n, m, state)

        # DEPLOY
        self.landList.sort(key=lambda x: x.value, reverse=True)
        cnt = 0
        max_val = self.landList[0].value
        for land in self.landList:
            if land.value < max_val:
                break
            cnt += 1
        for i in range(cnt):
            self.landList[i].add_soldier(int(self.number_of_lands() / cnt))
            print("troops added in land ", self.landList[i].i, self.landList[i].j)
        self.landList[i].add_soldier(int(self.number_of_lands() % cnt))

    def valuation(self, n, m, state):
        for i in range(n):
            for j in range(m):
                state[i][j].value = 0
                state[i][j].value += 8 - len(state[i][j].adjacencylist)
                friendly_land_cnt = 0
                enemy_land_cnt = 0
                friendly_soldier_cnt = 0
                enemy_soldier_cnt = 0
                for land in state[i][j].adjacencylist:
                    if self.id == land.owner:
                        friendly_land_cnt += 1
                        friendly_soldier_cnt += land.soldiersCount
                    else:
                        enemy_soldier_cnt += land.soldiersCount
                        enemy_land_cnt += 1

                if state[i][j].owner == self.id:
                    state[i][j].value += 1 / state[i][j].soldiersCount
                    if friendly_land_cnt == 8:
                        state[i][j].value += -friendly_soldier_cnt
                    else:
                        friendly_land_cnt += 1
                        state[i][j].value += (1 / (
                                abs(
                                    4 - friendly_land_cnt) + 1)) * 10 - friendly_soldier_cnt / friendly_land_cnt + enemy_soldier_cnt / (enemy_land_cnt+1) - state[i][j].soldiersCount / (enemy_land_cnt+1)
                else:
                    friendly_land_cnt += 1
                    state[i][
                        j].value += friendly_land_cnt + friendly_soldier_cnt / friendly_land_cnt - enemy_soldier_cnt / (
                                enemy_land_cnt + 1)
                    state[i][j].value -= state[i][j].soldiersCount / 5
