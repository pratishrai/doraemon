import discord
import os
import asyncio
import prismapy
import random
from discord.ext import commands
from discord.utils import get
from discord.utils import find
import db
import env_file


client = commands.Bot(command_prefix="?")
analytics = prismapy.Prismalytics("2oZ3tPpluuZ3V0DtSqcEjQ", client, save_server=True)
client.remove_command('help')


@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online,
                                 activity=discord.Activity(name="You using my Gadgets", type=3))
    print(f'Bot is running as "{client.user.name}"')
    print("=========================================")


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    await client.process_commands(message)


@client.event
async def on_guild_join(guild):
    profile = {
        "guild_id": guild.id,
        "guild_name": guild.name,
        "prefix": '-',
        "welcome_channel": guild.system_channel,
        "welcome_message": "Hey {user.mention} welcome to {guild.name}",
        
    }

    db.add_guild(profile)
    channel = guild.system_channel
    embed = discord.Embed(
        title="Hello!",
        colour=0x2859b8,
        description="""Hello, I'm **Doraemon**. I am an all in one bot made by **The Good Kid#1999**. I can be used for Fun, Moderation and much more. My command prefix is `-`.
You can find all my command by typing `-help` and know more about me by typing `-about`. """)
    await channel.send(embed=embed)




@client.event
async def on_guild_remove(guild):
    db.remove_guild(guild.id)


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
    if isinstance(error, commands.CommandNotFound):
        pass
    elif isinstance(error, commands.MissingPermissions):
        pass


@client.command()
async def about(ctx):
    embed = discord.Embed(
        title="About",
        colour=0x2859b8,
        description="""Hello, I'm **Doraemon**,
I am not a 22nd century bot, I have been built in 21st century by [**Pratish**](http://programmingwizard.tech/).
I am a multi purpose bot. I can be used for Fun, Moderation and much more.
Use the `-help` command to know my commands and their functions.
""")
    await ctx.send(embed=embed)


@client.command()
async def help(ctx):
    embed = discord.Embed(
        title="Doraemon's commands:",
        colour=0x2859b8,
        description="""

**__General__**

`-about` - To know about the bot.
`-ping` - Check the bot's latency.
`-github` - Github Repo.
`-stats` - Check the bot's stats.
`-invite` - Get the invite link for the bot.

**__Fun__**

`-8ball <your question>` - Play magic 8 Ball and get the answers to all your questions.
`-meme` - Get a random meme from reddit.

**__Moderation__**

`-clear <amount of messages>` - Clears the specified no. of messages.(default=5)
`-kick <member> <reason>` - Kicks a member out of the server.
`-ban <member> <reason>` - Bans a member in the server.
`-unban <member>` - Unbans the member in the server.
`-count` - Count of messages in a channel.
`-info` - General Info of a member.

**__Other__**
`-lmgtfy <question>` -  Returns a [lmgtfy.com](https://lmgtfy.com/) link.
`-gif <query>` - Get a random GIF from tanor on the specified query.
""")
    await ctx.send(embed=embed)


@client.command()
async def ping(ctx):
    embed = discord.Embed(
        title="Ping",
        colour=0x2859b8,
        description=f'Pong! `Latency: {round(client.latency * 1000)} ms`')
    await ctx.send(embed=embed)


@client.command()
async def github(ctx):
    embed = discord.Embed(
        title="GitHub Repo",
        colour=0x2859b8,
        description="https://github.com/pratishrai/doraemon")
    await ctx.send(embed=embed)


@client.command()
async def invite(ctx):
    embed = discord.Embed(
        colour=0x2859b8,
        description="https://discord.com/api/oauth2/authorize?client_id=709321027775365150&permissions=8&scope=bot) me to your server")
    await ctx.send(embed=embed)



@client.command()
async def typing(ctx):
    async with ctx.channel.typing():
        await asyncio.sleep(5)
        await ctx.send('done!')



@client.event
async def on_command(ctx):
    await analytics.send(ctx)


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

token = env_file.get()

client.run(token['BOT_TOKEN'])
