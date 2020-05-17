import discord
import os
import requests
import random
import pyjokes
from discord.ext import commands
from discord.utils import find

client = discord.Client()
client = commands.Bot(command_prefix='-')
client.remove_command('help')


@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online,
                                 activity=discord.Activity(name="Nobita doing his homework.", type=3))
    print('The Bot is ready.')


@client.event
async def on_guild_join(guild):
    general = find(lambda x: x.name == 'general', guild.text_channels)
    if general and general.permissions_for(guild.me).send_messages:
        embed = discord.Embed(
            title="About",
            description="""Hello, I'm **Doraemon**,
I am a moderator bot. My command prefix is `-`. You can find all my commands by typing `-help` and know more about me by typing `-about`.
You must have the required permissions to use a certain command. I have some additional features which can be used by anyone.
Type `-perms` to know the permissions required to use a certain command.
""")
        await general.send(embed=embed)


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(
            title="Error",
            description="This command doesn't exist.")
        await ctx.send(embed=embed)


@client.command()
async def perms(ctx):
    embed = discord.Embed(
        title="Permissions",
        description="""
# Commands which require Perissions:

`-clear` - Manage Message Permission
`-kick` - Kick Members Permission
`-ban` - Ban Members Permission
`-unban` - Ban Members Permission

# Command which can be used by anyone:

`-ping`
`-joke`
`-8ball`
`-help`
`-about`
`-github`
`-count`

* Type `-help` to the function of each command.
""")
    await ctx.send(embed=embed)


@client.command()
async def about(ctx):
    embed = discord.Embed(
        title="About",
        description="""Hello, I'm **Doraemon**,
I am not a 22nd century bot, I have been built in 21st century by [**Pratish**](http://programmingwizard.tech/).
I am a moderation bot but I have some additional features too.
Type `-help` to see my commands.
Please [`invite`](https://discord.com/api/oauth2/authorize?client_id=709321027775365150&permissions=32668710&scope=bot) me to your server:
""")
    await ctx.send(embed=embed)


@client.command()
async def help(ctx):
    embed = discord.Embed(
        title="Doraemon's commands:",
        description="""
`-about` - To know about the bot.
`-ping` - Check the bot's latency.
`-stats` - Check the bot's statistics.
`-github` - Github Repo.
`-kick <member> <reason>` - Kicks a member out of the server.
`-ban <member> <reason>` - Bans a member in the server.
`-unban <member>` - Unbans the member in the server.
`-8ball <your question>` - Play magic 8 Ball and get the answers to all your questions.
`-joke` - A random joke.
`-clear <amount of messages>` - Clears the specified no. of messages.(default=5)
`-count` - Count of messages in a channel.
    """)
    await ctx.send(embed=embed)


@client.command()
async def ping(ctx):
    embed = discord.Embed(
        title="Ping",
        description=f'Pong! `Latency: {round(client.latency * 1000)} ms`')
    await ctx.send(embed=embed)


@client.command()
async def github(ctx):
    embed = discord.Embed(
        title="GitHub Repo",
        description="GitHub Repo:\n https://github.com/programming-wizard/doraemon")
    await ctx.send(embed=embed)


@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
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
        description=f'Question: {question}\nAnswer: {random.choice(responses)}')
    await ctx.send(embed=embed)


@client.command()
async def joke(ctx):
    embed = discord.Embed(
        title="Joke",
        description=f'{pyjokes.get_joke()}')
    await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)


@client.command(aliases=['yeet'])
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    embed = discord.Embed(
        title="Kicked",
        description=f'{member.mention} has been kicked.')
    await member.kick(reason=reason)
    await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    embed = discord.Embed(
        title="Banned",
        description=f'{member.mention} has been banned.')
    await member.ban(reason=reason)
    await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            embed = discord.Embed(
                title="Banned",
                description=f'{user.mention} has been unbanned.')
            await ctx.send(embed=embed)
            return


@client.command()
async def count(ctx, channel: discord.TextChannel = None):
    channel = channel or ctx.channel
    count = 0
    async for _ in channel.history(limit=None):
        count += 1
    embed = discord.Embed(
        title="Total Messages",
        description=f"There were {count} messages in {channel.mention}")
    await ctx.send(embed=embed)


@client.command()
async def spam(ctx, *, message):
    msg = message.split(' ')
    number = int(msg[-1])
    counter = 0
    while counter < number:
        await ctx.send(message)
        counter += 1


@client.event
async def on_command(ctx):
    message = ctx.message
    guild = message.guild
    print(guild.region)
    data = {'message': message.content, 'server': guild.name, 'member_count': guild.member_count,
            'server_region': guild.region}
    requests.post('https://prismalytics.herokuapp.com/send_data', data=data,
                  headers={'key': 'Secret Key'})


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run('Bot Token')
