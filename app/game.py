class Board():
    def __init__(self, height, width, food, snakes):
        self.height = height
        self.width = width
        self.food = food
        self.snakes = snakes

class Snake():
    def __init__(self, id, name, health, body):
        self.id = id
        self.name = name
        self.health = health
        self.body = body
        self.head = self.body[0]
        self.tail = self.body[-1]