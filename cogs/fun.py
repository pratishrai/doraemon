import discord
from discord.ext import commands
import requests
import json
import praw
import random
from discord.utils import get
import env_file

token = env_file.get()


reddit = praw.Reddit(
    client_id=f"{token['CLIENT_ID']}",
    client_secret=f"{token['CLIENT_SECRET']}",
    user_agent="doraemon by /u/pr0grammingwizard",
)


class Fun(commands.Cog, name="Fun"):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def joke(self, ctx):
        async with ctx.channel.typing():
            url = "https://icanhazdadjoke.com/"
            response1 = requests.get(url, headers={"Accept": "application/json"}).json()
            response2 = requests.get(
                "https://sv443.net/jokeapi/v2/joke/Miscellaneous,Dark?type=single"
            ).json()
            responses = [response1["joke"], response2["joke"]]
            joke = random.choice(responses)
            embed = discord.Embed(title="Joke", colour=0x2859B8, description=f"{joke}")
        await ctx.send(embed=embed)

    @commands.command(aliases=["8ball"])
    async def _8ball(self, ctx, *, question):
        async with ctx.channel.typing():
            responses = [
                "It is certain.",
                "As I see it, yes.",
                "Reply hazy, try again.",
                "Don't count on it.",
                "It is decidedly so.",
                "Most likely.",
                "Ask again later.",
                "My reply is no.",
                "Without a doubt.",
                "Outlook good.",
                "Better not tell you now.",
                "My sources say no.",
                "Yes – definitely.",
                "Yes.",
                "Cannot predict now.",
                "Outlook not so good.",
                "You may rely on it.",
                "Signs point to yes.",
                "Concentrate and ask again.",
                "Very doubtful.",
            ]
            embed = discord.Embed(
                title="Magic 8 Ball",
                colour=0x2859B8,
                description=f"Question: {question}\nAnswer: {random.choice(responses)}",
            )
        await ctx.send(embed=embed)

    @commands.command()
    async def meme(self, ctx):
        async with ctx.channel.typing():
            sub = random.choice(["memes", "dankmemes"])
            subreddit = reddit.subreddit(f"{sub}")
            memes = []
            for submission in subreddit.hot(limit=50):
                if not submission.stickied:
                    memes.append(submission)

            choice = random.choice(range(len(memes)))
            title = memes[choice].title
            url = memes[choice].url
            permalink = memes[choice].permalink
            embed = discord.Embed(
                colour=0x2859B8,
                description=f"**[{title}](https://www.reddit.com{permalink})**",
            )
            embed.set_image(url=f"{url}")
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Fun(client))
