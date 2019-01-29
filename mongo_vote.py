from pymongo import MongoClient

'''
Documentation:
find_by_id(id)
find_by_username(user)
find_by_choice(choice)
add_vote(user,choice,rank)
'''

class Mongo_Vote:
	class Vote:
		def __init__(self, i, user, position, votes):
			self.id = i
			self.user = user
			self.position = position
			self.votes = votes #votes is an dict of votes
			self.weight = 1
			
		def change_weight(new_weight):
			self.weight = new_weight

	def __init__(self):
		self.client = MongoClient('mongodb://localhost:27017/')
		self.collection = self.client.ramanujan.vote

	#Return Value: Single Vote
	def find_by_id(self, i):
		with self.client:
			json = self.collection.find({"_id": i})
			
			for v in json:
				return self.Vote(v["_id"], v["user"], v["position"], v["votes"])

			return None

	#Return Value: List of Votes
	def find_by_user(self, user):
		with self.client:
			json = self.collection.find({"user": user})
			
			lst_vote = []
			for v in json:
				lst_vote.append(self.Vote(v["_id"], v["user"], v["position"], v["votes"]))
			return lst_vote

	#Return Value: List of Votes
	def find_by_position(self, position):
		with self.client:
			json = self.collection.find({"position": position})
			
			lst_vote = []
			for v in json:
				lst_vote.append(self.Vote(v["_id"], v["user"], v["position"], v["votes"]))
			return lst_vote

	#Return Value: Single Vote
	def add_vote(self, user, position, votes):
		with self.client:
			json = self.collection.find({"user": user, "position": position})
			
			v = None
			for item in json:
				v = lst_vote.append(self.Vote(v["_id"], v["user"], v["position"], v["votes"]))

			if not v:
				result = self.collection.insert_one({"user":user, "position": position, "votes":votes})
				return self.Vote(result.inserted_id, user, position, votes)				
			else:
				raise ValueError("User already voted")
				return None