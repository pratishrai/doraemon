import dbl
import discord
from discord.ext import commands
import env_file

token = env_file.get()


class TopGG(commands.Cog):
    """Handles interactions with the top.gg API"""

    def __init__(self, client):
        self.client = client
        self.token = token["DBL_TOKEN"]
        self.dblpy = dbl.DBLClient(
            self.client, self.token, autopost=True
        )  # Autopost will post your guild count every 30 minutes

    @commands.Cog.listener()
    async def on_guild_post(self):
        print("Server count posted successfully")


def setup(client):
    client.add_cog(TopGG(client))
