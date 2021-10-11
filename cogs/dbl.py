import topgg
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()


class TopGG(commands.Cog):
    """Handles interactions with the top.gg API"""

    def __init__(self, client):
        self.client = client

        self.dbl_token = os.getenv("DBL_TOKEN")  # set this to your bot's Top.gg token

        self.client.topggpy = topgg.DBLClient(
            client, self.dbl_token, autopost=True, post_shard_count=True
        )

    @commands.Cog.listener()
    async def on_autopost_success(self):
        print(
            f"Posted server count ({self.client.topggpy.guild_count}), shard count ({self.client.shard_count})"
        )


def setup(client):
    client.add_cog(TopGG(client))
