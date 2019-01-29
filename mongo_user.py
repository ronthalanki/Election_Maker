from pymongo import MongoClient
import hashlib

'''
Documentation:
find_by_id(id)
find_by_username(username)
find_by_access_level(access_level)
get_all()
add_user(username, password, access_level)
change_password(username, password)
delete_user(username)
'''

def password_hash(password):
	return hashlib.sha512(password.encode('utf-8')).hexdigest()

class Mongo_User:
	class User:
		def __init__(self, i, username, password, access_level):
			self.id = i
			self.username = username
			self.password = password
			self.access_level = access_level

		def check_password(self, password):
			if password_hash(password) == self.password:
				return True
			return False
			
		def __str__(self):
			return "Username: " + self.username + ", Access Level: " + str(self.access_level)

	def __init__(self):
		self.client = MongoClient('mongodb://localhost:27017/')
		self.collection = self.client.ramanujan.user

	#Return Value: Single User
	def find_by_id(self, i):
		with self.client:
			json = self.collection.find({"_id": i})
			
			for u in json:
				return self.User(u["_id"], u["username"], u["password"], u["access_level"])

			return None

	#Return Value: Single User
	def find_by_username(self, username):
		with self.client:
			json = self.collection.find({"username": username})
			
			for u in json:
				return self.User(u["_id"], u["username"], u["password"], u["access_level"])

			return None

	#Return Value: List of Users
	def find_by_access_level(self, access_level):
		with self.client:
			json = self.collection.find({"access_level": access_level})
			
			lst_user = []
			for u in json:
				lst_user.append(self.User(u["_id"], u["username"], u["password"], u["access_level"]))
			
			return lst_user

	#Return Value: Single User
	def add_user(self, username, password, access_level):
		with self.client:
			usr = self.find_by_username(username)
			if not usr:
				result = self.collection.insert_one({"username": username, "password": password_hash(password), "access_level": access_level})
				return self.User(result.inserted_id, username, password_hash(password), access_level)
			else:
				raise ValueError("User already exists")
				return None

	#Return Value: Single User Object
	def change_password(self, username, password):
		with self.client:
			self.collection.update_one({"username":username},{"$set":{"password": password_hash(password)}})
			
			#checking if password actually changed
			u = self.find_by_username(username)
			if u.password != password_hash(password):
				raise ValueError("Password change not successful")

			return u

	#No Return Value
	def delete_user(self, username):
		with self.client:
			self.collection.delete_one({"username":username})

			#checking if user was successfully deleted
			u = self.find_by_username(username)
			if not u:
				raise ValueError("Deletion not successful")
