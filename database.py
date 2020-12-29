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
    guild = guild_profiles.find_one({"guild_id": guild})
    return guild


def find_member(member):
    member = member_profiles.find_one({"member_id": member})
    return member


def set_tz(member, tz):
    member_profiles.update_one({"member_id": member}, {"$set": {"tz": tz}})


def get_tz(member):
    member = member_profiles.find_one({"member_id": member})
    tz = member["tz"]
    return tz


"""
guild_profile = {
            "guild_id": message.guild.id,
            "bot_msg_channel": None,
            "welcome_channel": None,
            "welcome_message": "Hey {user.mention} welcome to {guild.name}",
            "welcome_type": "channel",
            "subreddits": ["memes", "dankmemes"],
            "autorole": False,
            "on_join_role": None,
            "greeting_type": "text"
        }
"""


def get_data(guild, data=None):
    if data is not None:
        guild = guild_profiles.find_one({"guild_id": guild})
        data = guild[f"{data}"]
        return data


def set_data(guild, data=None, value=None):
    if data and value is not None:
        guild_profiles.update_one({"guild_id": guild}, {"$set": {f"{data}": value}})


# guild_profiles.update_many(
#     {},
#     {"$set": {"welcome_message": "Hey {user.mention} welcome to {guild.name}"}},
#     upsert=False,
#     array_filters=None,
# )
