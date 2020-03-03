import json
import os
import random

import bottle
from bottle import HTTPResponse
from game import *


@bottle.route("/")
def index():
    return "Your Battlesnake is alive!"


@bottle.post("/ping")
def ping():
    """
    Used by the Battlesnake Engine to make sure your snake is still working.
    """
    return HTTPResponse(status=200)


@bottle.post("/start")
def start():
    """
    Called every time a new Battlesnake game starts and your snake is in it.
    Your response will control how your snake is displayed on the board.
    """
    data = bottle.request.json
    print("START:", json.dumps(data))

    response = {"color": "#a1223f", "headType": "bendr", "tailType": "curled"}
    return HTTPResponse(
        status=200,
        headers={"Content-Type": "application/json"},
        body=json.dumps(response),
    )


@bottle.post("/move")
def move():
    """
    Called when the Battlesnake Engine needs to know your next move.
    The data parameter will contain information about the board.
    Your response must include your move of up, down, left, or right.
    """
    data = bottle.request.json
    print("MOVE:", json.dumps(data))

    def GetSafeMoves(position, xWalls, yWalls, snakeSpots):
    #returns moves that go into an open space
        safeMoves = []
        counter = 0
        for location in GetNewLocations(position).values():
            if location not in player.body[:-1] and location['x'] not in xWalls and location['y'] not in yWalls and location not in snakeSpots:
                safeMoves.append(directions[counter])
            counter += 1
        return safeMoves

    def GetNewLocations(location):
    #returns a dictionary of the 4 possible moves as keys with the position they lead to as values
        newLocations = {}
        directions = ["up", "down", "left", "right"]
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
    
    def HasFood(location):
        if location in board.food:
            return True
        return False

    directions = ["up", "down", "left", "right"]
    board = Board(data['board']['height'], data['board']['width'], data['board']['food'], data['board']['snakes'])
    player = Snake(data['you']['id'], data['you']['name'], data['you']['health'], data['you']['body'])
    currentLocation = player.head
    # print("\n\n\n\n this is the current location: ", currentLocation, "\n\n\n")

    #wall locations
    xWalls = [-1, board.width]
    yWalls = [-1, board.height]

    snakeSpots = []
    if (len(board.snakes) > 0):
        for snake in board.snakes:
            snakeSpots += snake["body"]

    #choosing a move that doesn't kill us
    moves = GetSafeMoves(currentLocation, xWalls, yWalls, snakeSpots)
    mostDirectionsOpen = 0 #we want to choose the move that gives us the most options from there so we don't corner ourself
    goodMoves = []
    for option in moves:
    #this loop looks one move into the future and chooses the moves that leave the most spaces open to move into next
        directionsOpen = len(GetSafeMoves(GetNewLocations(currentLocation)[option], xWalls, yWalls, snakeSpots))
        print("\n directions open for ", option, " at ", GetNewLocations(currentLocation)[option], " is ", directionsOpen)
        if directionsOpen == mostDirectionsOpen:
            goodMoves.append(option)
        elif directionsOpen > mostDirectionsOpen:
            goodMoves = [option]
            mostDirectionsOpen = directionsOpen
    
    if player.health < 40:
    #prioritize finding food if all else is equal
        foodMoves = []
        for option in moves:
            if HasFood(GetNewLocations(currentLocation)[option]):
                foodMoves.append(option)
        if len(foodMoves) > 0:
            goodMoves = foodMoves
    print("\n good moves: ", goodMoves)
    # for key in directions:
    if len(moves) == 0:
        move = random.choice(directions)
    else:
        move = random.choice(goodMoves)

    # Shouts are messages sent to all the other snakes in the game.
    # Shouts are not displayed on the game board.
    shout = "I am a python snake!"

    response = {"move": move, "shout": shout}
    return HTTPResponse(
        status=200,
        headers={"Content-Type": "application/json"},
        body=json.dumps(response),
    )


@bottle.post("/end")
def end():
    """
    Called every time a game with your snake in it ends.
    """
    data = bottle.request.json
    print("END:", json.dumps(data))
    return HTTPResponse(status=200)


def main():
    bottle.run(
        application,
        host=os.getenv("IP", "0.0.0.0"),
        port=os.getenv("PORT", "8080"),
        debug=os.getenv("DEBUG", True),
    )


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == "__main__":
    main()
