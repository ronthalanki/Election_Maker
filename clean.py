from pymongo import MongoClient

#Initialize 5 users with 2 access levels, remove any votes
client = MongoClient('mongodb://localhost:27017/')
collection_user = client.ramanujan.user
collection_vote = client.ramanujan.vote
collection_election = client.ramanujan.election
collection_position = client.ramanujan.position
collection_choice = client.ramanujan.choice

collection_user.drop()
collection_vote.drop()
collection_election.drop()
collection_position.drop()
collection_choice.drop()

print("Finished cleaning data")