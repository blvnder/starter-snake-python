import utils

class Board():
    def __init__(self, data):
        self.height = data['board']['height']
        self.width = data['board']['width']
        self.food = data['board']['food']
        self.snakes = self.getSnakes(data)
        self.snakeSpots = self.getSnakeSpots()
        self.grid = self.makeGrid()
    
    # Create a grid of the current game state
    def makeGrid(self):
        grid = [[0 for col in range(self.width)] for row in range(self.height)]

        for grub in self.food:
            grid[grub['x']][grub['y']] = 2
        
        for spot in self.snakeSpots:
            grid[spot['x']][spot['y']] = 1
        
        return grid

    # Make a given move on the board
    def makeMove(self, move, location, player):
        # If there's food at the new location:
        # 1. Update board to mark cell with player body instead of food
        # 2. Set player health to maximum (100)
        # 3. Move player head into new location (thus extending length)
        newLocations = self.getNewLocations(location)
        loc = newLocations[move]
        if self.grid[loc['x']][loc['y']] == 2:
            self.grid[loc['x']][loc['y']] = 1
            player.health = 100
            player.body.insert(0, loc)
            player.head = loc
        # Otherwise:
        # 1. Update board to mark cell with player body
        # 2. Reduce player health by 1
        # 3. Move player head into new location
        # 4. Remove player tail from board
        self.grid[loc['x']][loc['y']] = 1
        player.health -= 1
        player.body.insert(0, loc)
        player.head = loc
        del player.body[-1]

    # Returns a list of all snake objects
    def getSnakes(self, data):
        snakes = []
        for snake in data['board']['snakes']:
            s = Snake(snake)
            snakes.append(s)
        return snakes
    
    # Returns a list of cells occupied by enemy snakes
    def getSnakeSpots(self, player=None):
        snakeSpots = []
        if len(self.snakes) > 0:
            for snake in self.snakes:
                if player is None:
                    snakeSpots += snake.body
                elif snake.id != player.id:
                    snakeSpots += snake.body
        return snakeSpots
    
    # Returns true if a given location is a valid move and false otherwise
    def isValid(self, location, player):
        # print("New location:", location)
        # Check for out of bounds
        if location['x'] < 0 or location['x'] > self.width-1 or location['y'] < 0 or location['y'] > self.height-1:
            # print("Out of bounds")
            return False
        # Check for collision with other snakes
        snakeSpots = self.getSnakeSpots(player)
        if location in snakeSpots:
            # print("Enemy collision")
            return False
        # Check for collision with self (excluding tail)
        if location in player.body[:-1]:
            # print("Self collision")
            return False
        # print("Valid move")
        return True
    
    # Get coordinates of moves in all directions
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

    # Get a list of legal moves for the current game state
    def getLegalMoves(self, location, player):
        legalMoves = []
        moves = self.getNewLocations(location)
        for key, value in moves.items():
            # print("Current location:", location)
            if self.isValid(value, player) == False:
                continue
            legalMoves.append(key)
        # print("Legal Moves:", legalMoves)
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