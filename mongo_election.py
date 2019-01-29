from pymongo import MongoClient

'''
Documentation:
find_by_id(id)
find_by_user(user)
add_election(name, user)
'''

class Mongo_Election:
	class Election:
		def __init__(self, i, name, user):
			self.id = i
			self.name = name
			self.user = user
			
	def __init__(self):
		self.client = MongoClient('mongodb://localhost:27017/')
		self.collection = self.client.ramanujan.election

	#Return Value: Single Election
	def find_by_id(self, i):
		with self.client:
			json = self.collection.find({"_id": i})
			
			for e in json:
				return self.Election(e["_id"], e["name"], e["user"])

			return None	

	#Return Value: List of Elections
	def find_by_user(self, user):
		with self.client:
			json = self.collection.find({"user": user})
			
			lst_election = []
			for e in json:
				lst_election.append(self.Election(e["_id"], e["name"], e["user"]))
			return lst_election

	#Return Value: Single Election
	def add_election(self, name, user):
		with self.client:
			json = self.collection.find({"name": name, "user": user})

			elect = None
			for e in json:
				elect = self.Election(e["_id"], e["name"], e["user"])

			if not elect:
				result = self.collection.insert_one({"name": name, "user": user})
				return self.Election(result.inserted_id, name, user)
			else:
				raise ValueError("Election already exists")
				return None