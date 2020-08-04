import discord
from discord.ext import commands
import requests
import json
import random


class Others(commands.Cog, name="Others"):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def lmgtfy(self, ctx, *, question):
        ques = question.replace(" ", "+")
        link = f"https://lmgtfy.com/?q={ques}"
        embed = discord.Embed(
            colour=0x2859b8,
            description=f"{link}")
        await ctx.send(embed=embed)

    @commands.command()
    async def gif(self, ctx, *, query):
        gif_object = requests.get(f"https://api.tenor.com/v1/search?q={query}&key=9NHL3US0DWU0&limit=50").json()
        choice = random.choice(range(len(gif_object["results"])))
        url = gif_object['results'][choice]['url']
        
        await ctx.send(url)

    


def setup(client):
    client.add_cog(Others(client))
