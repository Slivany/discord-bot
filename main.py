# Import libraries
import shutil
import discord
import aiohttp
import os
import aiofiles
from discord.ext import commands
import random
import praw
import tokens

# Connects the bot to Discord, and set its prefix as well as removing the default help command.
Client = discord.Client()
client = commands.Bot(description="This bot has a variety of funny commands", command_prefix="!")
client.remove_command('help')


@client.event
async def on_ready():
    print("Bot is online and connected to Discord")


# Imports our private IDs **THOSE MUST BE KEPT SECRET**
reddit = praw.Reddit(client_id=tokens.clientID,
                     client_secret=tokens.clientSecret,
                     user_agent=tokens.userAgent)


# Catching a 'command not found' warning that would get spammed otherwise
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.author.send(error + ' | No command called `{}`'.format(ctx.command))
        return
    print('Catching command not found error')


# Defines a command that posts a random image from the hot section in the Awwnime subreddit,
# selected randomly, using the Praw library.
@client.command()
async def aww():
    awwnime_submissions = reddit.subreddit('awwnime').hot()
    post_to_pick = random.randint(1, 20)
    for i in range(0, post_to_pick):
        submission = next(x for x in awwnime_submissions if not x.stickied)

    await client.say(submission.url)


pic_ext = ['.jpg', '.png', '.jpeg']


# Defines a bunch of commands using our prefix
@client.event
async def on_message(message):
    # Lists all of the available commands with a small description
    if message.content.upper().startswith('!HELP'):
        await client.send_message(message.channel, "**Commands:**\n!help - lists all commands\n"
                                                   "!aww - posts a random image from the awwnime subreddit\n"
                                                   "!say - make me say anything\n"
                                                   "!poke - don't you dare poke me!\n"
                                                   "!gamble - get a random number from 1 to 100\n"
                                                   "!ratemywaifu - insert an image URL of your waifu and have it rated\n"
                                                   "!download - downloads image URl with a given tag\n"
                                                   "!addtag - adds another image tag to work in conjunction with the download command\n"
                                                   "!deltag - deletes specificed image tag and all of its content\n"
                                                   "!showtags - shows all of the tags that has currently been made\n"
                                                   "!usetag - posts a random image that has been paired with the specified tag\n"
                                                   "Do `!syntax command-name` for further help")

    # Lists the proper way to use a command based of the second string labeled after !syntax
    if message.content.upper().startswith('!SYNTAX'):
        args = message.content.split(" ")
        if args[1] == 'aww':
            await client.send_message(message.channel, "Use the command as follows: `!aww`")
        elif args[1] == 'help':
            await client.send_message(message.channel, "Use the command as follows: `!help`")
        elif args[1] == 'say':
            await client.send_message(message.channel, "Use the command as follows: `!say arbitrary-sentence`")
        elif args[1] == 'poke':
            await client.send_message(message.channel, "Use the command as follows: `!poke`")
        elif args[1] == 'gamble':
            await client.send_message(message.channel, "Use the command as follows: `!gamble`")
        elif args[1] == 'ratemywaifu':
            await client.send_message(message.channel, "Use the command as follows: `!ratemywaifu image-url`")
        elif args[1] == 'download':
            await client.send_message(message.channel, "Use the command as follows: `!download image-tag image-url`")
        elif args[1] == 'addtag':
            await client.send_message(message.channel, "Use the command as follows: `!addtag image-tag`")
        elif args[1] == 'deltag':
            await client.send_message(message.channel, "Use the command as follows: `!deltag image-tag`")
        elif args[1] == 'showtags':
            await client.send_message(message.channel, "Use the command as follows: `!showtags`")

    # Picks one of random response whenever the !poke command is used
    if message.content.upper().startswith('!POKE'):
        userID = message.author.id
        await client.send_message(message.channel, random.choice(["<@%s> Stop it!" % (userID),
                                                                  "<@%s> Just can't help yourself?" % (userID),
                                                                  "<@%s> You know I'm an admin, right?" % (userID),
                                                                  "<@%s> Do you mind?" % (userID),
                                                                  "<@%s> What a dumbass.." % (userID)]))

    # Inputs a message with whatever is defined after the used !say command
    if message.content.upper().startswith('!SAY'):
        args = message.content.split(" ")
        await client.send_message(message.channel, "%s" % (" ".join(args[1:])))

    # Sends a message with a random number from 1 to a 100
    if message.content.upper().startswith('!GAMBLE'):
        userID = message.author.id
        await client.send_message(message.channel, "<@%s> " % (userID) + str(random.randint(1, 100)))

    # Picks a random response if the the second string labeled ends with .png, jpg or jpeg
    if message.content.upper().startswith('!RATEMYWAIFU'):
        for ext in pic_ext:
            if message.content.endswith(ext):
                userID = message.author.id
                await client.send_message(message.channel, random.choice(["<@%s> Trash-tier waifu" % (userID),
                                                                          "<@%s> Horrible, you should be ashamed" % (userID),
                                                                          "<@%s> Pretty average" % (userID),
                                                                          "<@%s> That ain't it chief" % (userID),
                                                                          "<@%s> That's pretty good!" % (userID),
                                                                          "<@%s> Wow, what a goddess" % (userID),
                                                                          "<@%s> Waifu of the year!" % (userID),
                                                                          "<@%s> I'd say it's fine" % (userID),
                                                                          "<@%s> Great, I see that you're a man of culture" % (userID),
                                                                          "<@%s> Eh, mediocre" % (userID),
                                                                          "<@%s> Damn, amazing" % (userID)]))

    # Creates a folder based of the second string labeled after the !addtag command
    if message.content.upper().startswith('!ADDTAG'):
        try:
            args = message.content.split(" ")
            tagDir = 'tag/' + args[1]
            tagName = args[1]
            os.mkdir(tagDir)
            await client.send_message(message.channel, "The tag **`" + tagName + "`** has been created.")
        except FileExistsError:
            await client.send_message(message.channel, "The tag **`" + tagName + "`** already exists! Try again.")

    # Deletes a folder based of the second string labeled after the !deltag command
    if message.content.upper().startswith('!DELTAG'):
        try:
            args = message.content.split(" ")
            delTagDir = 'tag/' + args[1]
            delTagName = args[1]
            shutil.rmtree(delTagDir)
            await client.send_message(message.channel, "The tag **`" + delTagName + "`** has been removed.")
        except FileNotFoundError:
            await client.send_message(message.channel, "The tag **`" + delTagName + "`** Does not exist! Try again.")

    if message.content.upper().startswith('!SHOWTAGS'):
        await client.send_message(message.channel, os.listdir('tag/'))

    # Posts a random image from a folder based of the second string labeled after the !usetag command
    if message.content.upper().startswith('!USETAG'):
        try:
            args = message.content.split(" ")
            useTagDir = args[1]
            randomTag = random.choice(os.listdir("tag\\" + useTagDir))
            await client.send_file(message.channel, "tag\\""" + useTagDir + "/{}".format(randomTag))
        except FileNotFoundError:
            await client.send_message(message.channel,
                                      "The tag does not exist, or the tag is not associated with any images. Try again.")
        except IndexError:
            await client.send_message(message.channel,
                                      "The tag does not appear to be paired with any images. Try again.")

    # Says something in response to a user tagging the bot
    if message.content.startswith("<@558191268572823572>"):
        await client.send_message(message.channel, "Greetings lost lamb. Do `!help` to see what I can do.")

    # Download image URL in the specified folder with a random name
    if message.content.upper().startswith('!DOWNLOAD'):
        try:
            async with aiohttp.ClientSession() as session:
                args = message.content.split(" ")
                tag = args[1]
                url = args[2]
                imgName = str(random.randint(1, 9999999))
                async with session.get(url) as resp:
                    if resp.status == 200:
                        f = await aiofiles.open('tag/' + tag + '/' + imgName + '.png', mode='wb')
                        await f.write(await resp.read())
                        await f.close()
                        await client.send_message(message.channel,
                                                  "The image has been downloaded with the tag **`" + tag + "`**.")
        except IndexError:
            await client.send_message(message.channel,
                                      "The tag is not valid, or no tag has been defined at all. Try again.")
        except ValueError:
            await client.send_message(message.channel,
                                      "The image could not be found. Try another URL.")
        except FileNotFoundError:
            await client.send_message(message.channel,
                                      "The tag is not valid, or no tag has been defined at all. Try again.")

    await client.process_commands(message)


# Run our client with the private Discord bot token **MUST NOT BE SHARED**
client.run(tokens.token)
