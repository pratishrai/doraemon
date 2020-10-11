import discord
from discord.ext import commands
from discord.utils import get
import os
import json
import asyncio
import shutil
import youtube_dl


class Music(commands.Cog, name="Music"):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def join(self, ctx):
        global voice
        channel = ctx.message.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
        embed = discord.Embed(colour=0x2859B8, description=f"Joined {channel}")
        await ctx.send(embed=embed)

    @commands.command()
    async def leave(self, ctx):
        channel = ctx.message.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.disconnect()
            embed = discord.Embed(colour=0x2859B8, description=f"Left {channel}")
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Music(client))
