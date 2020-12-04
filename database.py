import pymongo
from pymongo import MongoClient
import env_file

token = env_file.get()
client = MongoClient(token["URI"])
db = client.doraemonbot
guild_profiles = db.guild_profiles
member_profiles = db.member_profiles


def guilds():
    guild = list(db.guild_profiles.find({}))
    return guild


def members():
    member = list(db.member_profiles.find({}))
    return member


def add_guild(profile):
    guild_profiles.insert_one(profile)


def add_member(profile):
    member_profiles.insert_one(profile)


def remove_guild(guild):
    guild_profiles.delete_one({"guild_id": guild})


def find_guild(guild):
    guild_profiles = guild_profiles.find_one({"guild_id": guild})
    return guild


def find_member(member):
    member = member_profiles.find_one({"member_id": member})
    return member


def set_tz(member, tz):
    member_profiles.update_one({"member_id": member}, {'$set': {"tz": tz}})


def get_tz(member):
    member = member_profiles.find_one({"member_id": member})
    tz = member["tz"]
    return tz


# print(members())
# print(guilds())

# profiles.update_many({}, {"$set": {"something": "idk"}}, upsert=False, array_filters=None)