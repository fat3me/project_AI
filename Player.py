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





