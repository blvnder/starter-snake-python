import json
import os
import random

import bottle
from bottle import HTTPResponse


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
    currentLocation = data["you"]["body"][0]
    print("\n\n\n\n this is the current location: ", currentLocation, "\n\n\n")

    #wall locations
    xWalls = [-1]
    xWalls.append(data["board"]["width"])
    yWalls = [-1]
    yWalls.append(data["board"]["height"])

    print("\n\n xWalls: ", xWalls, "\n\n")
    print("\n\n yWalls: ", yWalls, "\n\n")

    snakeSpots = []
    if (len(data["board"]["snakes"]) > 0):
        for snake in data["board"]["snakes"]:
            print("snake: ", snake)
            snakeSpots += snake["body"]

    newLocations = {}
    for direction in directions:
        newLocations[direction] = {}
    
    #determining where each move ends up
    newLocations["up"]["x"] = currentLocation["x"]
    newLocations["up"]["y"] = currentLocation["y"]-1
    newLocations["down"]["x"] = currentLocation["x"]
    newLocations["down"]["y"] = currentLocation["y"]+1
    newLocations["left"]["x"] = currentLocation["x"]-1
    newLocations["left"]["y"] = currentLocation["y"]
    newLocations["right"]["x"] = currentLocation["x"]+1
    newLocations["right"]["y"] = currentLocation["y"]

    #choosing a move that doesn't kill us
    moves = []
    counter = 0
    for location in newLocations.values():
        print("\n\n location: ", location, "\n\n")
        if location not in data["you"]["body"][:-1] and location['x'] not in xWalls and location['y'] not in yWalls and location not in snakeSpots:
            moves.append(directions[counter])
        counter += 1
    

    # for key in directions:
    if len(moves) == 0:
        move = "up"
    else:
        move = random.choice(moves)

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
