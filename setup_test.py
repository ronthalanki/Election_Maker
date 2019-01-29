from mongo_user import Mongo_User
from mongo_vote import Mongo_Vote
from mongo_election import Mongo_Election
from mongo_position import Mongo_Position
from mongo_choice import Mongo_Choice

import random

mongo_user = Mongo_User()
mongo_vote = Mongo_Vote()
mongo_election = Mongo_Election()
mongo_position = Mongo_Position()
mongo_choice = Mongo_Choice()

#Create users & 1 admin
user_voters = {}
for i in range(10):
	user_voters["User" + str(i)] = "password"
admin = mongo_user.add_user("rick", "admin", 1)
users = []

for u in user_voters:
	users.append(mongo_user.add_user(u, user_voters[u], 2))

print("Added Users")

#create an Election
e = mongo_election.add_election("Election 1", admin.id)

positions = []
positions.append(mongo_position.add_position("President", e.id, 1))
positions.append(mongo_position.add_position("Vice-President", e.id, 1))
positions.append(mongo_position.add_position("Secretary", e.id, 1))

choices = []
for p in positions:
	temp_choices = []
	temp_choices.append(mongo_choice.add_choice("Choice 1", p.id).id)
	temp_choices.append(mongo_choice.add_choice("Choice 2", p.id).id)
	temp_choices.append(mongo_choice.add_choice("Choice 3", p.id).id)
	temp_choices.append(mongo_choice.add_choice("Choice 4", p.id).id)
	choices.append(temp_choices)
print("Added Election Details")

random.seed(2) #setting up seed so generated votes are the same for every test
for u in users:
	for i in range(len(choices)): #iterate through list of positions 
		rank_lst = [j for j in choices[i]]
		random.shuffle(rank_lst)
		mongo_vote.add_vote(u.id, positions[i].id, rank_lst)
print("Added User Votes")

print("Finished setting up")