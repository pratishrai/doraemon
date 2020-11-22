import discord
import os
import asyncio
import prismapy
import random
from discord.ext import commands
from discord.utils import get
from discord.utils import find
import database
import env_file


client = commands.Bot(command_prefix="?")
analytics = prismapy.Prismalytics("2oZ3tPpluuZ3V0DtSqcEjQ", client, save_server=True)
client.remove_command("help")


@client.command()
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")


@client.event
async def on_ready():
    await client.change_presence(
        status=discord.Status.online,
        activity=discord.Activity(name="You using my Gadgets", type=3),
    )
    print(f'Bot is running as "{client.user.name}"')
    print("=========================================")


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    guild = database.find_guild(message.guild.id)
    # if guild is None:
    #     profile = {
    #         "guild_id": message.guild.id,
    #         "prefix": "-",
    #         "welcome_channel": None,
    #         "welcome_message": "Hey {user.mention} welcome to {guild.name}",
    #         "welcome_type": "channel",
    #         "subreddits": ["memes", "dankmemes"],
    #         "autorole": False,
    #         "on_join_role": None,
    #     }

    #     database.add_guild(profile)
    #     print(f"Profile has been created for {message.guild.name}:{message.guild.id}")
    await client.process_commands(message)


@client.event
async def on_guild_join(guild):
    channel = guild.system_channel
    embed = discord.Embed(
        colour=0x2859B8,
        description="""Hello, Thanks for adding Doraemon!
        Doraemon is a multipurpose Discord Bot that has the commands commonly used on every server. It can also helps you do a lot of things right in discord.
        
        There are a lot of things you can do with Doraemon. Simply use the `-help` command to see a list of commands you can use.
        """,
    )
    embed.add_field(
        name="**__Usefull Links__**",
        inline=False,
        value="""
    Consider upvoting **[Doraemon](https://top.gg/bot/709321027775365150)** on Top.gg
    Have an issue/suggestion? Join the **[Support Server](https://discord.gg/yMkdWMg)**
    You can find the source code on **[Doraemon's GitHub page](https://github.com/pratishrai/doraemon)**
    """,
    )
    await channel.send(embed=embed)


# @client.event
# async def on_guild_remove(guild):
#     database.remove_guild(guild.id)


@client.event
async def on_member_join(member):
    channel = member.guild.system_channel
    if member.guild.id == 699037304836063292:
        print(f"Hey {member.mention}, Welcome to {member.guild}")
    else:
        await channel.send(f"Hey {member.mention}, Welcome to {member.guild}")


def is_it_me(ctx):
    return ctx.author.id == 690922103712776202


@client.event
async def on_command_error(ctx, error):
    print(error)


@client.command()
async def about(ctx):
    async with ctx.channel.typing():
        embed = discord.Embed(
            title="About",
            colour=0x2859B8,
            description="""Hello, I'm **Doraemon**,
I am not a 22nd century bot, I have been built in 21st century by [**Pratish**](http://programmingwizard.tech/).
I am a multi purpose bot. I can be used for Fun, Moderation and much more.
Use the `-help` command to know my commands and their functions.
""",
        )
    await ctx.send(embed=embed)


@client.group()
async def help(ctx):
    if ctx.invoked_subcommand is None:
        async with ctx.channel.typing():
            embed = discord.Embed(
                title="Help",
                colour=0x2859B8,
                description="""
    Here's the list of commands you can use:
    """,
            )
            embed.add_field(
                name="**__General__**", value="```about\nping\ngithub\nstats\ninvite```"
            )
            embed.add_field(
                name="**__Fun__**", value="```8ball\nmeme\ngif\n-joke\n-```"
            )
            embed.add_field(
                name="**__Reactions__**",
                value="```laugh\nshrug\nhug\ncry\npat\n```",
            )
            embed.add_field(
                name="**__Moderation__**",
                value="```clear\nkick\nban\nunban\ncount\ninfo\nserverinfo\n```",
            )
            embed.add_field(
                name="**__Utility__**", value="```lmgtfy\npoll\nreddit\n-\n-\n-\n-```"
            )
        await ctx.send(embed=embed)


@help.command()
async def help(ctx):
    async with ctx.channel.typing():
        embed = discord.Embed(
            colour=0x2859B8,
        )
        embed.add_field(name="Command", value="-help")
        embed.add_field(name="Alias", value="None")
        embed.add_field(
            name="Usage", inline=False, value="Shows the list of commands available"
        )
        embed.add_field(
            name="Example",
            inline=False,
            value="`-help <command name>`\n`-help poll`",
        )
    await ctx.send(embed=embed)


@help.command()
async def about(ctx):
    async with ctx.channel.typing():
        embed = discord.Embed(
            colour=0x2859B8,
        )
        embed.add_field(name="Command", value="-about")
        embed.add_field(name="Alias", value="None")
        embed.add_field(name="Usage", inline=False, value="Know more about the bot")
        embed.add_field(
            name="Example",
            inline=False,
            value="`-about",
        )
    await ctx.send(embed=embed)


@help.command()
async def ping(ctx):
    async with ctx.channel.typing():
        embed = discord.Embed(
            colour=0x2859B8,
        )
        embed.add_field(name="Command", value="-ping")
        embed.add_field(name="Alias", value="None")
        embed.add_field(name="Usage", inline=False, value="Check bot's latency")
        embed.add_field(
            name="Example",
            inline=False,
            value="`-ping`",
        )
    await ctx.send(embed=embed)


@help.command()
async def github(ctx):
    async with ctx.channel.typing():
        embed = discord.Embed(
            colour=0x2859B8,
        )
        embed.add_field(name="Command", value="-github")
        embed.add_field(name="Alias", value="`-gh`")
        embed.add_field(name="Usage", inline=False, value="Bot's Github Repo")
        embed.add_field(
            name="Example",
            inline=False,
            value="`-github`\n`-gh`",
        )
    await ctx.send(embed=embed)


@help.command()
async def stats(ctx):
    async with ctx.channel.typing():
        embed = discord.Embed(
            colour=0x2859B8,
        )
        embed.add_field(name="Command", value="-stats")
        embed.add_field(name="Alias", value="None")
        embed.add_field(name="Usage", inline=False, value="Check the bot's statistics")
        embed.add_field(
            name="Example",
            inline=False,
            value="`-stats`",
        )
    await ctx.send(embed=embed)


@help.command()
async def invite(ctx):
    async with ctx.channel.typing():
        embed = discord.Embed(
            colour=0x2859B8,
        )
        embed.add_field(name="Command", value="-invite")
        embed.add_field(name="Alias", value="None")
        embed.add_field(
            name="Usage", inline=False, value="Get the invite link for the bot"
        )
        embed.add_field(
            name="Example",
            inline=False,
            value="`-invite`",
        )
    await ctx.send(embed=embed)


# @help.command()
# async def help(ctx):
#     async with ctx.channel.typing():
#         embed = discord.Embed(
#             colour=0x2859B8,
#         )
#         embed.add_field(name="Command", value="")
#         embed.add_field(name="Alias", value="")
#         embed.add_field(name="Usage", inline=False, value="")
#         embed.add_field(
#             name="Example",
#             inline=False,
#             value="",
#         )
#     await ctx.send(embed=embed)


# @help.command()
# async def help(ctx):
#     async with ctx.channel.typing():
#         embed = discord.Embed(
#             colour=0x2859B8,
#         )
#         embed.add_field(name="Command", value="")
#         embed.add_field(name="Alias", value="")
#         embed.add_field(name="Usage", inline=False, value="")
#         embed.add_field(
#             name="Example",
#             inline=False,
#             value="",
#         )
#     await ctx.send(embed=embed)


# @help.command()
# async def help(ctx):
#     async with ctx.channel.typing():
#         embed = discord.Embed(
#             colour=0x2859B8,
#         )
#         embed.add_field(name="Command", value="")
#         embed.add_field(name="Alias", value="")
#         embed.add_field(name="Usage", inline=False, value="")
#         embed.add_field(
#             name="Example",
#             inline=False,
#             value="",
#         )
#     await ctx.send(embed=embed)


# @help.command()
# async def help(ctx):
#     async with ctx.channel.typing():
#         embed = discord.Embed(
#             colour=0x2859B8,
#         )
#         embed.add_field(name="Command", value="")
#         embed.add_field(name="Alias", value="")
#         embed.add_field(name="Usage", inline=False, value="")
#         embed.add_field(
#             name="Example",
#             inline=False,
#             value="",
#         )
#     await ctx.send(embed=embed)


# @help.command()
# async def help(ctx):
#     async with ctx.channel.typing():
#         embed = discord.Embed(
#             colour=0x2859B8,
#         )
#         embed.add_field(name="Command", value="")
#         embed.add_field(name="Alias", value="")
#         embed.add_field(name="Usage", inline=False, value="")
#         embed.add_field(
#             name="Example",
#             inline=False,
#             value="",
#         )
#     await ctx.send(embed=embed)


@client.command()
async def ping(ctx):
    async with ctx.channel.typing():
        embed = discord.Embed(
            title="Ping",
            colour=0x2859B8,
            description=f"Pong! `Latency: {round(client.latency * 1000)} ms`",
        )
    await ctx.send(embed=embed)


@client.command(aliases=["gh"])
async def github(ctx):
    async with ctx.channel.typing():
        embed = discord.Embed(
            title="GitHub Repo",
            colour=0x2859B8,
            description="https://github.com/pratishrai/doraemon",
        )
    await ctx.send(embed=embed)


@client.command()
async def invite(ctx):
    async with ctx.channel.typing():
        embed = discord.Embed(
            colour=0x2859B8,
            description="Invite me to your server using [this link](https://discord.com/api/oauth2/authorize?client_id=709321027775365150&permissions=8&scope=bot)",
        )
    await ctx.send(embed=embed)


@client.event
async def on_command(ctx):
    await analytics.send(ctx)


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")

token = env_file.get()

client.run(token["DEV_BOT_TOKEN"])