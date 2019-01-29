from flask import Flask, render_template, request, redirect, url_for 
from bson import ObjectId
from pymongo import MongoClient
import os

from mongo_choice import Mongo_Choice
from mongo_position import Mongo_Position
from mongo_election import Mongo_Election
from mongo_user import Mongo_User
from mongo_vote import Mongo_Vote

app = Flask(__name__)

collection_choice = Mongo_Choice()
collection_position = Mongo_Position() 
collection_election = Mongo_Election()
collection_user = Mongo_User()
collection_vote = Mongo_Vote()

def redirect_url():
    return request.args.get('next') or \
           request.referrer or \
           url_for('index')

@app.route("/")
def start_page():
	return render_template('login.html')

def index():
	user_id = request.values.get("user")
	raise NotImplementedError

#TODO: how to have user logged in for whole session, pass a session id to other calls?
@app.route("/login", methods=['POST'])
def login():
	username = request.values.get("username")
	password = request.values.get("password")

	user = collection_user.find_by_username("rick")

	if (user.check_password(password)):
		return render_template('index.html', user = str(user.id))
	else:
		return redirect("/")

def make_election():
	raise NotImplementedError

def vote():
	raise NotImplementedError

@app.route("/add_user", methods=['POST'])
def add_user():
	username = request.values.get("username")
	password = request.values.get("password")
	collection_user.add_user(username, password, 2)
	return redirect("/")

@app.route("/results")
def get_election_results():
	user_id = request.values.get("user")
	lst_election = collection_election.find_by_user(ObjectId(user_id))
	lst_position = collection_position.find_by_election(lst_election[0].id)
	
	return_val = []

	for p in lst_position:
		temp_dict = {}

		choice = find_winner(p.id)
		temp_dict["name"] = p.text
		temp_dict["winner"] = collection_choice.find_by_id(choice).text
		return_val.append(temp_dict)

	return render_template('results.html',title="Results Page", election=str(lst_election[0].name), positions=return_val)

def find_winner(position, remove_choice_lst = []):
	choice_lst = collection_choice.find_by_position(position)
	vote_lst = collection_vote.find_by_position(position)
	
	choice_votes = {}
	for choice in choice_lst:
		choice_votes[choice.id] = 0

	while True:
		for choice in choice_votes:
			choice_votes[choice] = 0
		
		for vote in vote_lst:
			choice_votes[vote.votes[0]] += 1
		print(choice_votes)

		min_choice_votes = len(vote_lst)
		min_choice = None
		for choice in choice_votes:
			if choice_votes[choice] < min_choice_votes:
				min_choice_votes = choice_votes[choice]
				min_choice = choice
			elif choice_votes[choice] > len(vote_lst) / 2:
				return choice
		
		print(str(min_choice) + " was removed from the election")
		for vote in vote_lst:
			remove_index = -1
			for i in range(len(vote.votes)):
				if vote.votes[i] == min_choice:
					remove_index = i
			del vote.votes[remove_index]

		del choice_votes[min_choice]


if __name__ == "__main__":
    app.run()