import discord
from discord.ext import commands


class Music(commands.Cog, name="Music"):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def join(self, ctx):
        channel = ctx.message.author.voice.voice_channel
        await self.client.join_voice_channel(channel)

    @commands.command()
    async def yo(self, ctx):
        await ctx.send("Yo")


def setup(client):
    client.add_cog(Music(client))
