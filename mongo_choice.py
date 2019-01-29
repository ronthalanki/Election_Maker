from pymongo import MongoClient

'''
Documentation:
find_by_id(id)
find_by_position(position)
add_position(text, position)
'''

class Mongo_Choice:
	class Choice:
		def __init__(self, i, text, position):
			self.id = i
			self.text = text
			self.position = position
			
	def __init__(self):
		self.client = MongoClient('mongodb://localhost:27017/')
		self.collection = self.client.ramanujan.choice

	#Return Value: Single Choice
	def find_by_id(self, i):
		with self.client:
			json = self.collection.find({"_id": i})
			
			for c in json:
				return self.Choice(c["_id"], c["text"], c["position"])

			return None

	#Return Value: List of Choices
	def find_by_position(self, position):
		with self.client:
			json = self.collection.find({"position": position})
			
			lst_choice = []
			for c in json:
				lst_choice.append(self.Choice(c["_id"], c["text"], c["position"]))
			return lst_choice

	#Return Value: Single Choice
	def add_choice(self, text, position):
		with self.client:
			result = self.collection.insert_one({"text": text, "position": position})
			return self.Choice(result.inserted_id, text, position)