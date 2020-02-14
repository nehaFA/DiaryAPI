from flask import Flask, request, jsonify
from uuid import uuid4
from datetime import datetime
from flask_cors import CORS, cross_origin

import json

app = Flask(__name__)
CORS(app)
#cors allows your api to be called from other services, you need this to deploy an API to the web 

#make helper function
def load_db():
	with open ("database.JSON", "r") as f:
		database = json.load(f)
	return database
#look up and find the database file (read only)
#save as something or return it 

#another helper function 
def save_db(database):
#looking for something new to add to existing database
	with open("database.JSON", "w") as f:
		json.dump(database, f, indent=4) #f represents old databas
#json.dump over rides the f and the database.json file with the new file we passed into the function. 
#no need to return anyting in def save_db

#first endpoint - get all
@app.route("/diaryentry", methods=["GET"])
@cross_origin()
#this function above is used to protect endpoints from hackers 
def get_all_diary_entries():
	db = load_db()
	n_entries = len(db)
	response = {
		"message" : "Successfully got all diary entries!",
		"entries" : db,
		"count" : n_entries
	}
	return jsonify (response), 200
# i need a function to load my database
# then i need to make my database be JSON
# then i need to return the JSON to the user
# do i need to do anything else?

#second endpoint-get a specific one
@app.route("/diaryentry/<entryid>", methods=["GET"])
#< > represents that the data will later have data input in it
@cross_origin()
#this function above is used to protect endpoints from hackers 
def get_diary_entry(entryid):
# we need to load our database
# we need to search the database for our entry id
# we need to return the entry associated to entry id
# we want to return that entry to the user with a success message
# if that ID doesnt exist, let the user know their entry ID isnt available.
	db = load_db()
	entry = db.get(entryid)
	success_response = {
		"message" : "Found your entry!", 
		"entry" : entry,
		"entryid" : entryid
	}
	if entry is None:

		return jsonify({"message":f"Could not find your entry with id {entryid}"}), 404
	return jsonify(success_response), 200

#third endpoint-post one
@app.route("/diaryentry", methods=["POST"])
@cross_origin()
#this function above is used to protect endpoints from hackers 
def create_diary_entry():
	new_entry = json.loads(request.data)
#use request to get the data from the post request & equate it to any variable you want. 
#Use json.loads to make sure its properly formatted in json format we want
	db = load_db()
#preparing all the variables that will be used; 
#load_db is a function we defined earlier in the code since we knew we'd use it several times
	unique_id = str(uuid4())
#we wanted to create a unique id so we used a python extended library. we could have used any random number generator we wanted. which took us to the top where we did from uuid etc
	db[unique_id] = new_entry
#this line joined everything together. make a new entry unique id and make it equal to data.
	db[unique_id]["createdat"]= str(datetime.now())
#the way we declare a new key in a dictionary is through createdat. Were defining it as a string. Have to use [] whenever were referring to db.
	save_db(db)
#need to save it so we can overwrite our otiginal file. Works like load_db but instead of reading the file, we want to write. 
#save_db is then defined above
	response = {
		"message": "New entry created",
		"data": new_entry,
#were sending the data back because its good practice to give reassurance to the user so they can see what they did send to the API
		"id": unique_id
#we send them something new with the id so they know what they need if they want to call the data again
	}
	return jsonify(response), 201

#201 used for when new things created/post and are OK
#alternative for line 68!
#createdat = str(datetime.now())

#third endpoint pseudocode: 
# get the data from the post request
# save the data into a variable
# load the database
# give the new entry an ID using the internal python database
# add the new entry to the database
# give the new entry a timestamp
# return the new entry and a success message to the user












