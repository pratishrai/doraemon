import discord
from discord.ext import commands


class Moderation(commands.Cog, name="Moderation"):

    def __init__(self, client):
        self.client = client

    
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount, before=ctx.message)
        await ctx.message.delete()
    

    @commands.command(aliases=['yeet'])
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        embed = discord.Embed(
            title="Kicked",
            colour=0x2859b8,
            description=f'{member.mention} has been kicked.')
        await member.kick(reason=reason)
        await ctx.send(embed=embed)


    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        embed = discord.Embed(
            title="Banned",
            colour=0x2859b8,
            description=f'{member.mention} has been banned.')
        await member.ban(reason=reason)
        await ctx.send(embed=embed)


    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                embed = discord.Embed(
                    title="Banned",
                    colour=0x2859b8,
                    description=f'{user.mention} has been unbanned.')
                await ctx.send(embed=embed)
                return
        embed = discord.Embed(
            title="None",
            colour=0x2859b8,
            description=f'No such user was found banned.')
        await ctx.send(embed=embed)

    @commands.command()
    async def count(self, ctx, channel: discord.TextChannel = None):
        channel = ctx.channel
        messages = await channel.history(limit=None).flatten()
        count = len(messages)
        embed = discord.Embed(
            title="Total Messages",
            colour=0x2859b8,
            description=f"There were {count} messages in {channel.mention}")
        await ctx.send(embed=embed)


    @commands.command()
    async def info(self, ctx, member: discord.Member = None):
        member = ctx.author if not member else member
        roles = [role for role in member.roles]

        embed = discord.Embed(color=member.color, timestamp=ctx.message.created_at)

        embed.set_author(name=f"User Info - {member}")
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

        embed.add_field(name="ID:", value=member.id)
        embed.add_field(name="Name:", value=member.display_name)

        embed.add_field(name=f"Created at:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
        embed.add_field(name=f"Joined at:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))

        embed.add_field(name=f"Roles({len(roles)})", value=" ".join([role.mention for role in roles]))
        embed.add_field(name="Top role: ", value=member.top_role.mention)

        embed.add_field(name="Bot? ", value=member.bot)

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Moderation(client))
