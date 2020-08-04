import discord
from discord.ext import commands


class Music(commands.Cog, name="Music"):

    def __init__(self, client):
        self.client = client



def setup(client):
    client.add_cog(Music(client))
