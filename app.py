from flask import Flask, request

# now we import the db.py file as a module
from db import genres, collection

# we import the Python module for random uuid's PS: they are not really random, they are unique
import uuid

# dince we're working with flask-smorest we use abort for our return statement
from flask_smorest import abort

app = Flask(__name__)

"""genres = [
    {
        "genre": "Fighting-games",
        "collection": [
            {"name": "Dragon-ball-fighterZ", "fav-char": "Android 19"},
            {"genre": "Guitly-Gear-Strive", "fav-char": "Nagoriyuki"},
        ],
    },
    {
        "genre": "FPS",
        "Collection": [
            {
                "name": "Call-of-Duty-Mobile",
                "fav-skin": "Iskra White Chappel",
                "fav-gun": "DLQ",
            }
        ],
    },
]

"""
# Now we refactor the games by using UUID's
# we would place them in a different Python file
# we would use a dictionary since we have to just reference the key than iterating through

""" GENRES """


# get all the genres
@app.get("/genres")
def retrieve_all_genres():
    return {
        "genres": list(
            genres.values()
        )  # PS: imma leave this here :) i got confused earlier; so, the values is from the "name" being the KEY and the values of it the VALUES
    }  # we turn genre.values() into a list in order to get the json format


# lets get the genre of a specific game
@app.get("/genres/<string:genre_id>")
def retrieve_specific_genre(genre_id):
    try:
        return genres[genre_id], 200
    except KeyError:
        abort(404, message="Genre is not ready")


# adding our own genre and collection(if we want)
@app.post("/genres")
def create_genre():
    genre_data = request.get_json()

    # error handoling to ensure a name is given to the game exception
    if "name" not in genre_data:
        abort(400, message="Add a name to the genre")

    # error handling to for the duplicate genres exceptiion
    for gen in genres.values():
        if genre_data["name"] == gen["name"]:
            abort(400, message="Genre of that name already exists")

    genre_id = uuid.uuid4().hex
    new_genre = {
        **genre_data,
        "id": genre_id,
    }  # the ** is to unpack the info in genre_data into kwargs
    genres[genre_id] = new_genre

    return new_genre, 201


"""# delete all gnere
@app.delete("/genres")
def delete_all_genre():
    try:
        del genres
        return {"message": "All genres deleted."}
    except KeyError:
        abort(404, message="All genres not deleted.")
"""


# delete a specific gnere
@app.delete("/genres/<string:genre_id>")
def delete_specific_genre(genre_id):
    try:
        del genres[genre_id]
        return {"message": "Genre has been deleted."}
    except KeyError:
        abort(404, message="No specific genre deleted.")


""" COLLECTION """


# get all the collection
@app.get("/collection")
def retrieve_all_collection():
    return {"collection": list(collection.values())}


# get the collection of a specific collection
@app.get("/collection/<string:collection_id>")
def retrieve_specific_collection(collection_id):
    try:
        return collection[collection_id], 200
    except KeyError:
        abort(404, message="Collection is not found")


# add a colection
@app.post("/collection")
def create_collection():
    collection_data = request.get_json()

    # adding the error handling for exeptions
    if "name" not in collection_data:
        abort(400, message="Ensure 'name' or 'fav-char' or 'fav-gun' is available")

    # handling duplicates
    for col in collection.values():
        if collection_data["name"] == col["name"]:
            abort(400, message="the data already exists")

    if collection_data["genre_id"] not in genres:
        abort(404, message="Genre not added")

    collection_id = uuid.uuid4().hex
    new_collection = {**collection_data, "id": collection_id}
    collection[collection_id] = new_collection

    return new_collection, 201


# update a collection
@app.put("/collection/<string:collection_id>")
def update_collection(collection_id):
    collection_data = request.get_json()

    # error so we fil all the collection requirement
    if "name" not in collection_data:
        abort(404, message="No collection of such name")
    try:
        new_collection = collection[collection_id]
        new_collection |= collection_data
        return new_collection
    except KeyError:
        abort(404, message="Collection not found")


"""# delete all collections
@app.delete("/collection")
def delete_all_collection():
    try:
        del collection
        return {"message": "All collections deleted succesfully"}
    except KeyError:
        abort(404, message="All collections not deleted.")"""


# delete specific collection
@app.delete("/collection/<string:collection_id>")
def delete_specific_collection(collection_id):
    try:
        del collection[collection_id]
        return {"message": "Item deleted"}
    except KeyError:
        abort(404, message="Collection is not found")
