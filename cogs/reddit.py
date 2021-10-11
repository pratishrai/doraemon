import discord
from discord.ext import commands
import requests
import os
import json
import praw
import random
import base64
from discord.utils import get
from dotenv import load_dotenv

load_dotenv()


reddit = praw.Reddit(
    client_id=f"{os.getenv('APP_ID')}",
    client_secret=f"{os.getenv('APP_SECRET')}",
    user_agent="doraemon by /u/pr0grammingwizard",
)


class Fun(commands.Cog, name="Fun"):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["m"])
    async def meme(self, ctx):
        async with ctx.channel.typing():
            sub = random.choice(["memes", "dankmemes"])
            subreddit = reddit.subreddit(f"{sub}")
            memes = []
            for submission in subreddit.hot(limit=100):
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

    @commands.command(aliases=["r"])
    async def reddit(self, ctx, *, search: str):
        search = search.split("|")
        subreddit = search[0]
        post = search[1:]
        subreddit = reddit.subreddit(f"{subreddit.strip()}")
        posts = []
        for post in subreddit.search(f"{post[0].strip()}", limit=5):
            posts.append(post)

        embed = discord.Embed(
            colour=0x2859B8,
            title=f"**https://www.reddit.com/r/{subreddit}**",
        )
        for i in posts:
            embed.add_field(
                name=f"{i.title}",
                inline=False,
                value=f"[Read the post here](https://www.reddit.com{i.permalink})\n --------------------------------------",
            )
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Fun(client))
