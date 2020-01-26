class Node:

    def __init__(self, main_player, player, next_player, moves, value, parent, isTerminal):
        self.player = player
        self.next_player = next_player
        self.value = value
        self.moves = moves
        self.parent = parent
        self.isTerminal = isTerminal
        self.main_player = main_player
        self.childs = []

    def calculate_utility(self, n, m):
        player = self.main_player
        res = 0
        for land in player.landList:
            res += land.value * land.soldiersCount

        self.value = res / (n * m - len(player.landList) + 0.00001)
        return res / (n * m - len(player.landList) + 0.00001)

