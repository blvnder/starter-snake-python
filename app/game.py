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

class Player(Snake):
    def __init__(self, id, name, health, body):
        super().__init__(id, name, health, body)

    def getSafeMoves(self, position, directions, xWalls, yWalls, snakeSpots):
    #returns moves that go into an open space
        safeMoves = []
        counter = 0
        for location in self.getNewLocations(position, directions).values():
            if location not in self.body[:-1] and location['x'] not in xWalls and location['y'] not in yWalls and location not in snakeSpots:
                safeMoves.append(directions[counter])
            counter += 1
        return safeMoves

    def getNewLocations(self, position, directions):
    #returns a dictionary of the 4 possible moves as keys with the position they lead to as values
        newLocations = {}
        for direction in directions:
            newLocations[direction] = {}
        newLocations["up"]["x"] = position["x"]
        newLocations["up"]["y"] = position["y"]-1
        newLocations["down"]["x"] = position["x"]
        newLocations["down"]["y"] = position["y"]+1
        newLocations["left"]["x"] = position["x"]-1
        newLocations["left"]["y"] = position["y"]
        newLocations["right"]["x"] = position["x"]+1
        newLocations["right"]["y"] = position["y"]
        return newLocations