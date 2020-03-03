class Board():
    def __init__(self, height, width, food, snakes):
        self.height = height
        self.width = width
        self.food = food
        self.snakes = snakes
    
    # Returns a list of enemy snake objects
    def getSnakes (self, data):
        enemies = []
        for snake in self.snakes:
            s = Snake(snake['id'], snake['name'], snake['health'], snake['body'])
            if s.id != data['you']['id']:
                append.enemies(s)
        return enemies
    
    # Returns a list of cells occupied by enemy snakes
    def getSnakeSpots(self, data):
        snakeSpots = []
        if (len(self.snakes) > 0):
            snakeList = self.getSnakes(data)
            for snake in snakeList:
                snakeSpots += snake.body
        return snakeSpots

class Snake():
    def __init__(self, id, name, health, body):
        self.id = id
        self.name = name
        self.health = health
        self.body = body
        self.head = self.body[0]
        self.tail = self.body[-1]