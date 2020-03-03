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

    directions = ["up", "down", "left", "right"]
    board = Board(data['board']['height'], data['board']['width'], data['board']['food'], data['board']['snakes'])
    player = Player(data['you']['id'], data['you']['name'], data['you']['health'], data['you']['body'])

    #wall locations
    xWalls = [-1, board.width]
    yWalls = [-1, board.height]

    snakeSpots = board.getSnakeSpots(data)

    #choosing a move that doesn't kill us
    moves = player.getSafeMoves(player.head, directions, xWalls, yWalls, snakeSpots)
    mostDirectionsOpen = 0 #we want to choose the move that gives us the most options from there so we don't corner ourself
    goodMoves = []
    for option in moves:
    #this loop looks one move into the future and chooses the moves that leave the most spaces open to move into next
        directionsOpen = len(player.getSafeMoves(player.getNewLocations(player.head, directions)[option], directions, xWalls, yWalls, snakeSpots))
        # print("\n directions open for ", option, " at ", GetNewLocations(currentLocation)[option], " is ", directionsOpen)
        if directionsOpen == mostDirectionsOpen:
            goodMoves.append(option)
        elif directionsOpen > mostDirectionsOpen:
            goodMoves = [option]
            mostDirectionsOpen = directionsOpen

    # print("\n good moves: ", goodMoves)
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
