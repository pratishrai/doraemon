import pymongo
from pymongo import MongoClient
import env_file

token = env_file.get()
client = MongoClient(token["URI"])
db = client.doraemonbot
profiles = db.guild_profiles

def guilds():
	guild = list(db.guild_profiles.find({}))
	return guild


def add_guild(profile):
    profiles.insert_one(profile)


def remove_guild(guild):
    profiles.delete_one({"guild_id": guild})



def find_guild(guild):
	guild = profiles.find_one({"guild_id": guild})
	return guild

# print(find_guild(876827316982))

# add_guild(profile)
# profiles.update_many({}, {"$set": {"something": "idk"}}, upsert=False, array_filters=None)