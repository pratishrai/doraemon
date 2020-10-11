import pymongo
from pymongo import MongoClient
import env_file

token = env_file.get()
client = MongoClient(token["URI"])
db = client.doraemonbot
profiles = db.guild_profiles

guild = list(db.guild_profiles.find({}))
print(guild)


def add_guild(profile):
    profiles.insert_one(profile)


def remove_guild(guild):
    profiles.delete_one({"guild_id": guild})


def delete():
    profiles.delete_one({"guild_id": 45654165198465163})


# delete()
# add_guild(profile)