import discord
from discord.ext import commands


class Moderation(commands.Cog, name="Moderation"):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["c"])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=1):
        await ctx.channel.purge(limit=amount, before=ctx.message + 1)

    @commands.command(aliases=["yeet"])
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        embed = discord.Embed(
            title="Kicked",
            colour=0x2859B8,
            description=f"{member.mention} has been kicked.",
        )
        await member.kick(reason=reason)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        embed = discord.Embed(
            title="Banned",
            colour=0x2859B8,
            description=f"{member.mention} has been banned.",
        )
        await member.ban(reason=reason)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                embed = discord.Embed(
                    title="Banned",
                    colour=0x2859B8,
                    description=f"{user.mention} has been unbanned.",
                )
                await ctx.send(embed=embed)
                return
        embed = discord.Embed(
            title="None", colour=0x2859B8, description=f"No such user was found banned."
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def info(self, ctx, member: discord.Member = None):
        async with ctx.channel.typing():
            member = ctx.author if not member else member
            roles = [role for role in member.roles]

            embed = discord.Embed(color=member.color, timestamp=ctx.message.created_at)

            embed.set_author(name=f"User Info - {member}")
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_footer(
                text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url
            )

            embed.add_field(name="ID:", value=member.id)
            embed.add_field(name="Name:", value=member.display_name)

            embed.add_field(
                name=f"Created at:",
                value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),
            )
            embed.add_field(
                name=f"Joined at:",
                value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),
            )

            embed.add_field(
                name=f"Roles({len(roles)})",
                value=" ".join([role.mention for role in roles]),
            )
            embed.add_field(name="Top role: ", value=member.top_role.mention)

            embed.add_field(name="Bot? ", value=member.bot)

        await ctx.send(embed=embed)

    @commands.command(aliases=["sinfo"])
    async def serverinfo(self, ctx):
        async with ctx.channel.typing():
            embed = discord.Embed(color=0x2859B8, timestamp=ctx.message.created_at)
            embed.set_author(name=f"Guild Info - {ctx.guild}")
            embed.set_thumbnail(url=ctx.guild.icon_url)
            embed.set_footer(
                text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url
            )
            embed.add_field(name="ID:", value=ctx.guild.id)
            embed.add_field(name="Owner:", value=ctx.guild.owner)
            embed.add_field(
                name=f"Created at:",
                value=ctx.guild.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),
            )
            embed.add_field(name=f"Region:", value=ctx.guild.region)
            embed.add_field(
                name=f"Verification Level", value=ctx.guild.verification_level
            )
            embed.add_field(name="Members", value=len(ctx.guild.members))
            embed.add_field(name="Channels", value=len(ctx.guild.channels))
            embed.add_field(name="Emojis", value=len(ctx.guild.emojis))
            embed.add_field(name="Roles", value=len(ctx.guild.roles))

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Moderation(client))
