from flask import Flask, request

app = Flask(__name__)

games_types = [
    {
        "name": "Fighting-games",
        "collection": [
            {"name": "Dragon-ball-fighterZ", "fav-char": "Android 19"},
            {"name": "Guitly-Gear-Strive", "fav-char": "Nagoriyuki"},
        ],
    },
    {
        "name": "FPS",
        "Collection": [
            {
                "name": "Call-of-Duty-Mobile",
                "fav-skin": "Iskra White Chappel",
                "fav-gun": "DLQ",
            }
        ],
    },
]


# get the games
@app.get("/games")
def retrieve_games():
    return {"games": games_types}


# lets get the type of game,  its name and the collection
@app.get("/games/<string:name>")
def retrieve_game_type(name):
    for game in games_types:
        if game["name"] == name:
            return {"game": game}, 200
    return {"message": "Collection is not ready"}, 404
