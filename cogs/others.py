import discord
from discord.ext import commands
import requests
import json
import random
import env_file


class Others(commands.Cog, name="Others"):
    def __init__(self, client):
        self.client = client

    def tenor(self, query):
        token = env_file.get()
        gif_object = requests.get(
            f"https://api.tenor.com/v1/search?q={query}&key={token['TENOR_KEY']}&limit=50"
        ).json()
        choice = random.choice(range(50))
        url = gif_object["results"][choice]["media"][0]["gif"]["url"]
        return url

    @commands.command()
    async def lmgtfy(self, ctx, *, question):
        async with ctx.channel.typing():
            ques = question.replace(" ", "+")
            link = f"https://lmgtfy.com/?q={ques}"
            embed = discord.Embed(colour=0x2859B8, description=f"{link}")
        await ctx.send(embed=embed)

    @commands.command(aliases=["g"])
    async def gif(self, ctx, *, query):
        async with ctx.channel.typing():
            url = self.tenor(query=query)
            embed = discord.Embed(colour=0x2859B8)
            embed.set_image(url=url)
        await ctx.send(embed=embed)

    @commands.command()
    async def laugh(self, ctx):
        async with ctx.channel.typing():
            url = self.tenor(query="laugh")
            embed = discord.Embed(title=f"{ctx.author.name} laughs", colour=0x2859B8)
            embed.set_image(url=url)
        await ctx.send(embed=embed)

    @commands.command()
    async def shrug(self, ctx):
        async with ctx.channel.typing():
            url = self.tenor(query="shrug")
            embed = discord.Embed(title=f"{ctx.author.name} shrugs", colour=0x2859B8)
            embed.set_image(url=url)
        await ctx.send(embed=embed)

    @commands.command()
    async def hug(self, ctx, *, user: discord.Member):
        async with ctx.channel.typing():
            url = self.tenor(query="hug")
            embed = discord.Embed(
                title=f"{ctx.author.name} hugs {user.name}", colour=0x2859B8
            )
            embed.set_image(url=url)
        await ctx.send(embed=embed)

    @commands.command()
    async def cry(self, ctx):
        async with ctx.channel.typing():
            url = self.tenor(query="cry")
            embed = discord.Embed(title=f"{ctx.author.name} cries", colour=0x2859B8)
            embed.set_image(url=url)
        await ctx.send(embed=embed)

    @commands.command()
    async def pat(self, ctx, *, user: discord.Member):
        async with ctx.channel.typing():
            url = self.tenor(query="pat")
            embed = discord.Embed(
                title=f"{ctx.author.name} pats {user.name}", colour=0x2859B8
            )
            embed.set_image(url=url)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Others(client))
