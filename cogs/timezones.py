from datetime import datetime

import dateparser
import discord
import pytz
from discord.ext import commands
import database

COMMON_TIMEZONES = {
    "IST": "Asia/Kolkata",
    "GMT": "UTC",
    "JPT": "Asia/Tokyo",
    "QBT": "America/Vancouver",
}


class TimezoneCommands(commands.Cog, name="Timezones"):
    def __init__(self, bot):
        self.bot = bot

    def get_tzname(self, tzname):
        if tzname is None:
            return

        if tzname.upper() in COMMON_TIMEZONES:
            return COMMON_TIMEZONES[tzname.upper()]

        return tzname

    async def get_or_create_tz_role(self, guild, tzname):
        role = discord.utils.get(guild.roles, name=tzname)
        if role is not None:
            return role

        role = await guild.create_role(name=tzname, reason="Created timezone role.")
        return role

    @commands.command(name="selftimezone", aliases=["selftz", "mytz"])
    async def self_timezone(self, ctx, tzname=None):
        """
        Set your own default timezone.
        """
        tzname = self.get_tzname(tzname)

        if tzname is None:
            return await ctx.send(f"Usage: `{ctx.prefix}{ctx.command} <timezone name>`")

        if tzname not in pytz.all_timezones:
            return await ctx.send(
                "Not a valid timezone!\n"
                "Must be properly capitalized ex: US/Eastern, Asia/Kolkata etc.\n"
                "Here is a list of Timezones you can refer to: https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568"
            )
        if tzname in pytz.all_timezones:
            database.set_tz(ctx.author.id, tzname)
        await ctx.send(f"Assigned timezone: {tzname}")

    @commands.command(name="time", aliases=["now"])
    async def get_time(self, ctx, tzname=None):
        """
        Get time for yourself or a member or for a timezone.
        """
        tzname = self.get_tzname(tzname)
        user = None

        if tzname not in pytz.all_timezones:
            if tzname is None:
                user = ctx.author
            elif len(ctx.message.mentions) > 0:
                user = ctx.message.mentions[0]
            else:
                user = discord.utils.find(
                    lambda u: u.name.lower() == tzname.lower()
                    or u.display_name.lower() == tzname.lower(),
                    ctx.guild.members,
                )
            if user is None:
                return await ctx.send("No such user found!")

            tzname = database.get_tz(user.id)

            if tzname is None:
                if user == ctx.author:
                    return await ctx.send(
                        f"You do not have default timezone set! Use `{ctx.prefix}selftimezone`"
                    )
                else:
                    return await ctx.send(
                        f"{user} does not have default timezone set! Use `{ctx.prefix}selftimezone`"
                    )

        tz = pytz.timezone(tzname)
        tz_now = datetime.now(tz)

        if user is not None:
            msg = f"Current time for {user} (timezone: {tzname}) is:"
        else:
            msg = f"Current time for timezone {tzname} is:"

        fmt = "%Y-%m-%d %H:%M:%S"

        await ctx.send(
            f"{msg} {tz_now.strftime(fmt)}\nUTC Time: {datetime.utcnow().strftime(fmt)}"
        )

    @commands.command(name="convert")
    async def convert_time(self, ctx, dtstring=None, to=None, from_=None):
        """
        Convert time from one timezone to another.
        """
        if dtstring is None or to is None:
            return await ctx.send(
                f"Usage: `{ctx.prefix}{ctx.command} <datetime string> <to timezone> [optional: from timezone]`"
            )

        user_tzname = database.get_tz(ctx.author.id)

        if from_ is None and user_tzname is None:
            return await ctx.send(
                f"You do not have default timezone set! Use `{ctx.prefix}selftimezone`"
            )
        elif from_ is None:
            from_ = user_tzname

        from_ = self.get_tzname(from_)
        to = self.get_tzname(to)

        if from_ not in pytz.all_timezones or to not in pytz.all_timezones:
            return await ctx.send("Timezone doesn't exist!")

        dp = dateparser.DateDataParser(
            languages=["en"],
            settings={
                "TIMEZONE": from_,
                "RETURN_AS_TIMEZONE_AWARE": True,
                "RELATIVE_BASE": datetime.now(pytz.timezone(from_)),
            },
        )

        dateobj = dp.get_date_tuple(dtstring).date_obj

        if dateobj is None:
            return await ctx.send("Cannot parse date/time!")

        fmt = "%Y-%m-%d %H:%M:%S"

        embed = discord.Embed(
            title="Time Conversion",
            colour=0x2859B8,
        )
        embed.add_field(name=f"From ({from_})", value=dateobj.strftime(fmt))
        embed.add_field(
            name=f"To ({to})", value=dateobj.astimezone(pytz.timezone(to)).strftime(fmt)
        )

        if user_tzname is not None:
            curr_time = datetime.now(pytz.timezone(user_tzname)).strftime(fmt)
            embed.set_footer(
                icon_url=ctx.author.avatar_url_as(size=64),
                text=f"Current time for {ctx.author.display_name}: {curr_time}",
            )

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(TimezoneCommands(client))
