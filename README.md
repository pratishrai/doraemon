[![Discord Bots](https://top.gg/api/widget/status/709321027775365150.svg)](https://top.gg/bot/709321027775365150)
[![invite bot](https://img.shields.io/static/v1?style=flat&logo=discord&logoColor=FFF&label=&message=invite%20bot&color=7289DA)](https://top.gg/bot/709321027775365150)

# Doraemon
**Doraemon provides the essentials used most commonly in servers. This includes easy to use, concise commands for administration and moderation, as well as multimedia management from various platforms like reddit. These usually require a number of different bots, so we aim to be a one-stop solution to make the server a great place to hang out much easier.**  

[![Discord Bots](https://top.gg/api/widget/709321027775365150.svg)](https://top.gg/bot/709321027775365150)


# Bot Commands

**General**

`-ping` - Check the bot's latency.  
`-github` - Github Repo.  
`-stats` - Check the bot's stats.  
`-invite` - Get the invite link for the bot.  

**Fun**

`-meme` - Get a random meme from reddit.  
`-gif <query>` - Get a random GIF from tenor on the specified query.  

**Reactions**

`-laugh`
`-shrug`
`-hug <user>`
`-cry`
`-pat <user>`

**Moderation**

`-clear <amount of messages>` - Clears the specified no. of messages.(default=1)  
`-kick <member> <reason>` - Kicks a member out of the server.  
`-ban <member> <reason>` - Bans a member from the server.  
`-unban <member>` - Unbans the member from the server.  
`-info` - General Info of a member.  
`-serverinfo` - General Info of the Server  

**Utility**

`-lmgtfy <question>` -  Returns a [lmgtfy.com](https://lmgtfy.com/) link.  
`-poll <title>|<description>|<option 1>|<option 2>|<option n>` - Create polls on [StrawPoll](https://strawpoll.com/) right in discord.  
`-reddit <subreddit>|<query>` - Search for posts in the specified subreddit.  
`-image <term>` - Search for Images from Unspalsh  

**Timezones**

`-selftz <timezone>` - Set you own default Timezone  
`-time <timezone/member>` - Get the current time for a timezone or a member.  
`-convert <time> <to tz> <from tz>` - Convert time in other timezones.  


# Setup

- Clone the repo with `git clone https://github.com/pratishrai/doraemon`
- Install the requirements using `pip3 install -r requirements.txt`
- Create a `.env` file with the following:
    > `BOT_TOKEN=<your bot token>`  
     `URI = <your mongodb URI>`  
     `TENOR_API = <your tenor API>`  
     `APP_ID = <your reddit application id>`  
     `APP_SECRET = <your reddit application secret>`  
     `STRAWPOLL_KEY = <your strawpoll api key>`  
     `DBL_TOKEN = <Top.gg Token>`  
     `ACCESS_KEY = <Unsplash Access Key>`  
     `ENVIRON = DEV`
- You can now run the bot using `python3 doraemon.py`


