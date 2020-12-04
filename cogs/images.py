import dbl
import discord
from discord.ext import commands
import env_file
import random
import requests

token = env_file.get()


class Images(commands.Cog):

    def __init__(self, client):
        self.client = client

    def images(self, query):
        response = requests.get(
            f"https://api.unsplash.com/search/photos/?client_id={token['ACCESS_KEY']}&query={query}&page=1&per_page=20"
        ).json()
        choice = random.choice(range(len(response["results"])))
        image = response["results"][choice]["urls"]["regular"]
        title = response["results"][choice]["description"]
        return image, title


    @commands.command(aliases=["img"])
    async def image(self, ctx, *, search: str):
        async with ctx.channel.typing():
            img, title = self.images(search)
            embed = discord.Embed(title=title,
                colour=0x2859B8)
            embed.set_image(url=img)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Images(client))