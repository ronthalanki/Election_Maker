from pymongo import MongoClient

'''
Documentation:
find_by_id(id)
find_by_election(election)
add_position(text, election)
'''

class Mongo_Position:
	class Position:
		def __init__(self, i, text, election, num_winners):
			self.id = i
			self.text = text
			self.election = election
			self.num_winners = num_winners

	def __init__(self):
		self.client = MongoClient('mongodb://localhost:27017/')
		self.collection = self.client.ramanujan.position

	#Return Value: Single Position
	def find_by_id(self, i):
		with self.client:
			json = self.collection.find({"_id": i})
			
			for p in json:
				return self.Position(p["_id"], p["text"], p["election"], p["num_winners"])

			return None

	#Return Value: List of Positions
	def find_by_election(self, election):
		with self.client:
			json = self.collection.find({"election": election})
			
			lst_position = []
			for p in json:
				lst_position.append(self.Position(p["_id"], p["text"], p["election"], p["num_winners"]))
			return lst_position

	#Return Value: Single Position
	def add_position(self, text, election, num_winners):
		with self.client:
			result = self.collection.insert_one({"text": text, "election": election, "num_winners": num_winners})
			return self.Position(result.inserted_id, text, election, num_winners)