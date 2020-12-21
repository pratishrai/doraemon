import discord
from discord.ext import commands
import database


class Settings(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(aliases=["settings", "set"])
    async def setting(self, ctx):
        if ctx.invoked_subcommand is None:
            async with ctx.channel.typing():
                embed = discord.Embed(
                    title="Settings Aliases",
                    colour=0x2859B8,
                    description="""
                    `systemchannel` - `sysmsg`, `botmsg`, `sysch`
                    `welcometype` - None
                    `welcomechannel` - `welcome`
                    `welcomemsg` - None
                    `autorole` - `ar`
                    `onjoinrole` - None
                    `greetingtype` - `greet`, `greeting`""",
                )
                embed.set_footer(
                    text="**Use `-help settings` to know more about each setting**"
                )
            await ctx.send(embed=embed)

    @setting.command(aliases=["sysmsg", "botmsg", "sysch", "systemchannel"])
    @commands.has_permissions(administrator=True)
    async def system_channel(self, ctx, channel: discord.TextChannel = None):
        if channel is not None:
            async with ctx.channel.typing():
                database.set_data(
                    guild=ctx.guild.id, data="bot_msg_channel", value=channel.id
                )
            return await ctx.send(
                f"The bot message channel is set to {channel.mention}"
            )
        async with ctx.channel.typing():
            bot_channel_id = database.get_data(
                guild=ctx.guild.id, data="bot_msg_channel"
            )
            bot_channel = self.client.get_channel(bot_channel_id)
        await ctx.send(f"Current bot message channel is set to {bot_channel.mention}")

    @setting.command(aliases=["welcome", "welcomechannel"])
    @commands.has_permissions(administrator=True)
    async def welcome_channel(self, ctx, channel: discord.TextChannel = None):
        if channel is not None:
            async with ctx.channel.typing():
                database.set_data(
                    guild=ctx.guild.id, data="welcome_channel", value=channel.id
                )
            return await ctx.send(f"Welcome channel is set to {channel.mention}")
        async with ctx.channel.typing():
            welcome_channel_id = database.get_data(
                guild=ctx.guild.id, data="welcome_channel"
            )
            welcome_channel = self.client.get_channel(welcome_channel_id)
        await ctx.send(f"Current welcome channel is set to {welcome_channel.mention}")

    @setting.command(aliases=["welcomemsg"])
    @commands.has_permissions(administrator=True)
    async def welcome_msg(self, ctx, *, msg: str = None):
        if msg is not None:
            async with ctx.channel.typing():
                database.set_data(guild=ctx.guild.id, data="welcome_message", value=msg)
            return await ctx.send(f"Welcome message is set to {msg}")
        async with ctx.channel.typing():
            welcome_msg = database.get_data(guild=ctx.guild.id, data="welcome_message")
        await ctx.send(
            f"Current welcome message is ```\n"
            + welcome_msg
            + """\n```\n
While setting welcome message you can use variables like;
`{guild}` (will be replaced with the Server name.)
`{member.name}` (will be replaced with the name of the new member.)
`{member.mention}` (will ping the member.)
"""
        )

    @setting.command(aliases=["welcometype"])
    @commands.has_permissions(administrator=True)
    async def welcome_type(self, ctx, type_: str = None):
        if type_ is not None:
            type_ = type_.lower()
            if type_ == "channel" or type_ == "dm" or type_ == "none":
                async with ctx.channel.typing():
                    database.set_data(
                        guild=ctx.guild.id, data="welcome_type", value=type_
                    )
                return await ctx.send(f"Welcome type is set to `{type_}`")
            return await ctx.send(
                "The available welcome types are `channel`, `dm`, `None`"
            )
        async with ctx.channel.typing():
            type_ = database.get_data(guild=ctx.guild.id, data="welcome_type")
        await ctx.send(f"Current welcome type is `{type_}`")

    @setting.command(aliases=["ar"])
    @commands.has_permissions(administrator=True)
    async def autorole(self, ctx, option: str = None):
        if option is not None:
            option = option.lower()
            if option == "true":
                async with ctx.channel.typing():
                    database.set_data(guild=ctx.guild.id, data="autorole", value=True)
                return await ctx.send(
                    "Autorole has been set to `True`. Use `-settings onjoinrole <role>` to set the role."
                )
            if option == "false":
                async with ctx.channel.typing():
                    database.set_data(guild=ctx.guild.id, data="autorole", value=False)
                return await ctx.send("Autorole has been set to `False`.")
            return await ctx.send(
                "Autorole can only be set to either `True` or `False`"
            )
        async with ctx.channel.typing():
            autorole = database.get_data(guild=ctx.guild.id, data="autorole")
        await ctx.send(f"Currently autorole is set to `{autorole}`")

    @setting.command(aliases=["onjoinrole"])
    @commands.has_permissions(administrator=True)
    async def on_join_role(self, ctx, role: discord.Role = None):
        if role is not None:
            async with ctx.channel.typing():
                database.set_data(
                    guild=ctx.guild.id, data="on_join_role", value=role.id
                )
            return await ctx.send(f"On join role has been sent to {role.mention}")
        async with ctx.channel.typing():
            role_id = database.get_data(guild=ctx.guild.id, data="on_join_role")
            role = discord.utils.get(ctx.guild.roles, id=role_id)
        if role is not None:
            return await ctx.send(f"Currently on join role is set to {role.mention}")
        await ctx.send("-settings onjoinrole <role>")


    @setting.command(aliases=["greet", "greeting", "greetingtype"])
    @commands.has_permissions(administrator=True)
    async def greeting_type(self, ctx, _type: str=None):
        if _type is not None:
            _type = _type.lower()
            if _type == "text" or _type == "image":
                async with ctx.channel.typing():
                    database.set_data(guild=ctx.guild.id, data="greeting_type", value=_type)
                return await ctx.send(f"Greeting has been set to `{_type}`.")
            return await ctx.send(
                "Greeting can only be set to either `text` or `image`"
            )
        greeting = database.get_data(guild=ctx.guild.id, data="greeting_type")
        return await ctx.send(f"Greeting type is currenty set to `{greeting}`")


def setup(client):
    client.add_cog(Settings(client))