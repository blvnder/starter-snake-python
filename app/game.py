import utils

class Board():
    def __init__(self, data):
        self.height = data['board']['height']
        self.width = data['board']['width']
        self.food = data['board']['food']
        self.snakes = self.getSnakes(data)
        self.snakeSpots = self.getSnakeSpots()
        self.player = Snake(data['you'])
        self.grid = self.makeGrid()
    
    def makeGrid(self):
        grid = [[0 for col in range(self.width)] for row in range(self.height)]

        for grub in self.food:
            grid[grub['x']][grub['y']] = 2
        
        for spot in self.snakeSpots:
            grid[spot['x']][spot['y']] = 1
        
        return grid

    def makeMove(self, move, location, player):
        # If there's food at the move location
        newLocations = self.getNewLocations(location)
        loc = newLocations[move]
        if self.grid[loc['x']][loc['y']] == 2:
            self.grid[loc['x']][loc['y']] = 1
            player.health = 100
            player.body.insert(0, loc)
            player.head = loc
        self.grid[loc['x']][loc['y']] = 1
        player.health -= 1
        player.body.insert(0, loc)
        player.head = loc
        del player.body[-1]

    # Returns a list of enemy snake objects
    def getSnakes(self, data):
        enemies = []
        for snake in data['board']['snakes']:
            s = Snake(snake)
            if s.id != data['you']['id']:
                enemies.append(s)
        return enemies
    
    # Returns a list of cells occupied by enemy snakes
    def getSnakeSpots(self):
        snakeSpots = []
        if len(self.snakes) > 0:
            for snake in self.snakes:
                snakeSpots += snake.body
        return snakeSpots
    
    def isValid(self, location):
        if location['x'] < 0 or location['x'] > self.width-1 or location['y'] < 0 or location['y'] > self.height-1:
            return False
        if location in self.snakeSpots:
            return False
        if location in self.player.body[:-1]:
            return False
        return True
    
    def getNewLocations(self, location):
        directions = ["up", "down", "left", "right"]
        newLocations = {}
        for direction in directions:
            newLocations[direction] = {}
        newLocations["up"]["x"] = location["x"]
        newLocations["up"]["y"] = location["y"]-1
        newLocations["down"]["x"] = location["x"]
        newLocations["down"]["y"] = location["y"]+1
        newLocations["left"]["x"] = location["x"]-1
        newLocations["left"]["y"] = location["y"]
        newLocations["right"]["x"] = location["x"]+1
        newLocations["right"]["y"] = location["y"]
        return newLocations

    def getLegalMoves(self, location):
        legalMoves = []
        moves = self.getNewLocations(location)
        for key, value in moves.items():
            if self.isValid(value) == False:
                continue
            legalMoves.append(key)
        return legalMoves
            
    def isWin(self):
        for snake in self.snakes:
            if snake.head == self.player.head:
                if len(snake.body) < len(self.player.body):
                    return True
        return False

    def isLose(self):
        for snake in self.snakes:
            if snake.head == self.player.head:
                if len(snake.body) > len(self.player.body):
                    return True
        if self.player.health == 0:
            return True
        return False

class Snake():
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.health = data['health']
        self.body = data['body']
        self.head = self.body[0]
        self.tail = self.body[-1]