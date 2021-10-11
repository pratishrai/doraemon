import discord
from discord.ext import commands
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()


class Poll(commands.Cog, name="Poll"):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["sp", "poll"])
    async def strawpoll(self, ctx, *, poll_data: str):

        poll_data = poll_data.split("|")
        title = poll_data[0]
        options = poll_data[1:]

        data = {
            "poll": {
                "title": title,
                "description": "\u200b",
                "answers": options,
                "priv": True,
                "ma": 0,
                "mip": 0,
                "co": 1,
                "vpn": 0,
                "enter_name": 0,
                "has_deadline": False,
                "only_reg": 0,
                "has_image": 0,
                "image": None,
            }
        }

        poll = requests.post(
            "https://strawpoll.com/api/poll",
            json=data,
            headers={"API-KEY": os.getenv("STRAWPOLL_KEY")},
        ).json()

        await ctx.send(f"https://strawpoll.com/{poll['content_id']}")


def setup(client):
    client.add_cog(Poll(client))
