import discord
from discord.ext import commands
import env_file
import database
from PIL import Image, ImageDraw, ImageFont
import io
import aiohttp


token = env_file.get()


class JoinLeave(commands.Cog, name="Poll"):
    def __init__(self, client):
        self.client = client

    async def make_join_leave_image(self, image_url, header, subtitle):
        async with aiohttp.ClientSession() as session:
            async with session.get(str(image_url)) as resp:
                image_bytes = await resp.read()
        profile_pic = Image.open(io.BytesIO(image_bytes), "r")
        profile_pic = profile_pic.resize((160, 160), Image.ANTIALIAS)
        background = Image.open("assets/background.jpg", "r")
        font_1 = ImageFont.truetype("assets/DiscordFont.otf", 53)
        font_2 = ImageFont.truetype("assets/DiscordFont.otf", 48)
        bigsize = (profile_pic.size[0] * 3, profile_pic.size[1] * 3)
        mask = Image.new("L", bigsize, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + bigsize, fill=255)
        mask = mask.resize(profile_pic.size, Image.ANTIALIAS)
        profile_pic.putalpha(mask)
        background.paste(profile_pic, (350, 280), profile_pic)
        draw = ImageDraw.Draw(background)
        w, _ = draw.textsize(header, font=font_1)
        draw.text(((900 - w) / 2, 500), header, font=font_1)
        w, _ = draw.textsize(subtitle, font=font_2)
        draw.text(((900 - w) / 2, 580), subtitle, font=font_2)
        byte_io = io.BytesIO()
        background.save(byte_io, "PNG")
        byte_io.flush()
        byte_io.seek(0)
        return discord.File(fp=byte_io, filename="discord.png")

    async def send_on_member_join(self, member):
        welcome_type = database.get_data(guild=member.guild.id, data="welcome_type")
        greeting_type = database.get_data(guild=member.guild.id, data="greeting_type")
        if welcome_type != "none":
            welcome_msg = database.get_data(
                guild=member.guild.id, data="welcome_message"
            )
            welcome_msg = welcome_msg.replace("{guild}", member.guild.name)
            welcome_msg = welcome_msg.replace("{member.mention}", member.mention)
            welcome_msg = welcome_msg.replace(
                "{member}", f"{member.name}#{member.discriminator}"
            )
            if greeting_type == "image":
                img = await self.make_join_leave_image(
                    member.avatar_url_as(format="png", size=256),
                    "{0}#{1} has joined".format(
                        member.name, member.discriminator
                    ).capitalize(),
                    f"Welcome to {member.guild.name}",
                )
            if welcome_type == "channel":
                channel_id = database.get_data(
                    guild=member.guild.id, data="welcome_channel"
                )
                if channel_id is not None:
                    channel = self.client.get_channel(channel_id)
                    if greeting_type == "image":
                        return await channel.send(file=img)
                    return await channel.send(welcome_msg)
            if welcome_type == "dm":
                if greeting_type == "image":
                    return await member.send(file=img)
                return await member.send(welcome_msg)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await self.send_on_member_join(member=member)
        autorole = database.get_data(guild=member.guild.id, data="autorole")
        if autorole:
            on_join_role = database.get_data(guild=member.guild.id, data="on_join_role")
            if on_join_role is not None:
                role = discord.utils.get(member.guild.roles, id=on_join_role)
                return await member.add_roles(role)


def setup(client):
    client.add_cog(JoinLeave(client))
