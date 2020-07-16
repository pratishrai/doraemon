import discord
from discord.ext import commands
import requests
import json
import random


class Fun(commands.Cog, name="Fun"):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def joke(self, ctx):
        url = 'https://icanhazdadjoke.com/'
        response1 = requests.get(url, headers= {'Accept': 'application/json'}).json()
        response2 =requests.get("https://sv443.net/jokeapi/v2/joke/Miscellaneous,Dark?type=single").json()
        responses = [response1, response2]
        joke = random.choice(responses)
        embed = discord.Embed(
            title="Joke",
            colour=0x2859b8,
            description=f"{joke}")
        await ctx.send(embed=embed)


    @commands.command(aliases=['8ball'])
    async def _8ball(self, ctx, *, question):
        responses = [
            'It is certain.',
            'As I see it, yes.',
            'Reply hazy, try again.',
            "Don't count on it.",
            'It is decidedly so.',
            'Most likely.',
            'Ask again later.',
            'My reply is no.',
            'Without a doubt.',
            'Outlook good.',
            'Better not tell you now.',
            'My sources say no.',
            'Yes – definitely.',
            'Yes.',
            'Cannot predict now.',
            'Outlook not so good.',
            'You may rely on it.',
            'Signs point to yes.',
            'Concentrate and ask again.',
            'Very doubtful.',
        ]
        embed = discord.Embed(
            title="Magic 8 Ball",
            colour=0x2859b8,
            description=f'Question: {question}\nAnswer: {random.choice(responses)}')
        await ctx.send(embed=embed)


    @commands.command()
    async def udict(self, ctx, term):
        udict_def = requests.get(f'https://api.urbandictionary.com/v0/define?term={term}').json()
        choice = random.choice(range(len(udict_def.json()["list"])))
        term = udict_def["list"][choice]["word"]
        definition = udict_def["list"][choice]["definition"]
        author = udict_def["list"][choice]["author"]
        example = udict_def["list"][choice]["example"]
        thumbs_up = udict_def["list"][choice]["thumbs_up"]
        thumbs_down = udict_def["list"][choice]["thumbs_down"]
        permalink = udict_def["list"][choice]["permalink"]
        embed = discord.Embed(
            title="Urban Dictionary",
            colour=0x2859b8,
            description=f"**[{term}]({permalink})**")
        embed.add_field(name="**__Definition__**", value=f"{definition}")
        embed.add_field(name="**__Example__**", inline=False,
                        value=f"{example}")
        embed.add_field(name="**__Author__**", inline=False,
                        value=f"{author}")
        embed.add_field(name="**__Votes__**", value=f"{thumbs_up} :thumbsup: {thumbs_down} :thumbsdown:")
        await ctx.send(embed=embed)
        
        
    @commands.command()
    async def lmgtfy(self, ctx, *, question):
        ques = question.replace(" ", "+")
        link = f"https://lmgtfy.com/?q={ques}"
        embed = discord.Embed(
            colour=0x2859b8,
            description=f"{link}")
        await ctx.send(embed=embed)

    

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        with open("deleted.json") as f:
            messages = json.load(f)
        messages[str(message.channel.id)] = f"{message.content} ~{message.author}"
        with open('deleted.json', 'w') as f:
            json.dump(messages, f, indent=4)
        await self.client.process_commands(message)

    @commands.command()
    async def snipe(self, ctx):
        with open('deleted.json', 'r') as file:
            messages = json.load(file)

        message =  messages[str(ctx.channel.id)]
        embed = discord.Embed(
            colour=0x2859b8,
            description=f"{message}")
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Fun(client))
