# :robot: Doraemon
**A multipurpose Discord Bot that has the commands commonly used on every server, like Moderation, Fun, Playing Music and much more.**

[Invite the bot to your server](https://discord.com/api/oauth2/authorize?client_id=709321027775365150&permissions=8&scope=bot)

<ins>**Bot Commands**</ins>

**General**  

`-about` - To know about the bot.  
`-ping` - Check the bot's latency.  
`-github` - Github Repo.  
`-stats` - Check the bot's stats.  
`-invite` - Get the invite link for the bot.  

**Fun**  

`-8ball <your question>` - Play magic 8 Ball and get the answers to all your questions.  
`-meme` - Get a random meme from reddit.  

**Reactions**

`-laugh`
`-shrug`
`-hug <user>`
`-cry`
`-pat <user>`

**__Moderation__**  

`-clear <amount of messages>` - Clears the specified no. of messages.(default=5)  
`-kick <member> <reason>` - Kicks a member out of the server.  
`-ban <member> <reason>` - Bans a member in the server.  
`-unban <member>` - Unbans the member in the server.  
`-count` - Count of messages in a channel.  
`-info` - General Info of a member.  

**Other**  
`-lmgtfy <question>` -  Returns a [lmgtfy.com](https://lmgtfy.com/) link.  
`-gif <query>` - Get a random GIF from tanor on the specified query.  


<ins>**Coming Soon**</ins>

- Music
- Web Dashboard


<ins>**Setup**</ins>

- Clone the repo with `git clone https://github.com/pratishrai/doraemon`
- Install the requirements using `pip3 install -r requirements.txt`
- Create a `.env` file with the following:
    > `BOT_TOKEN=<your bot token>`  
     `URI=<your mongodb URI>`  
     `TENOR_API=<your tenor API>`  
     `CLIENT_ID=<your reddit application id>`  
     `CLIENT_SECRET=<your reddit application secret>`  
- You can now run the bot using `python3 doraemon.py`


