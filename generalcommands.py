import asyncio
import discord
from discord.ext.commands import Bot
from discord.ext import commands
import json
import random


#prints some help/syntax for users, can give specific help or return all commands
"""
@client.command()
async def commands(command="List of commands"):
        commandlist = {
"identify":["Usage: id <image URL>","Identifies up to 3 faces in an image and gives some data about them"],
"img":["Usage: img <search term> <result number>","Returns the corresponding image result for the query"],
"define":["Usage: define <word>","Gives the first definition for a word on bing"],
"toptracks":["Usage: toptracks <artist>","Returns the 5 most popular tracks from a given artist"],
"trackinfo":["Usage: trackinfo <track name>","Gives a link to the track and some information on it"] ,
"tracklist":["Usage: tracklist <album>","Embeds a spotify link to the album given"] ,
"artistinfo":["Usage: artistinfo <artist>","Returns some data about a given artist"] ,
"artistalbums":["Usage: artistalbums <artist>","Returns every album by a given artist"],
"playlists":["Usage: playlists <user>","Returns every public spotify playlist for a given user and the song count"] ,
"roll":["Usage: roll <upperbound>","Returns a random number form 1 to the upper bound"] ,
"game":["Usage: game","A really rubbish game where, there is an inverted tree with four rows. You choose left or right and you are aiming to get the lowest number while the computer wants to get the highest number. You can't win"],
"nuke":["Usage: please dont","Moves all users to the *graveyard* and nukes the bitrate of a channel"],
"toppost":["Usage: toppost <subreddit><time period>","Acceptable time periods: 'day' 'week' 'month' 'year' 'all'. Returns the top post from the subreddit given"],
"topcomment":["Usage: topcomment <user>","Returns a given user's top comment"],
"bottomcomment":["Usage: bottomcomment <user>","Returns a given user's bottom comment"],
"randomsub":["Usage: randomsub","Returns the top post from a random subreddit"],
"randnsfw":["Usage: randnsfw","Returns the top post from a random NSFW subreddit"],
"List of commands":["List of commands:","id \n img \n define \n toptracks \n trackinfo \n tracklist \n artistinfo \n artistalbums \n playlists \n roll \n game \n nuke \n toppost \n topcomment \n bottomcomment \n randomsub \n randnsfw"]}
        commandtitle = commandlist[command][0]
        commandsdesc = commandlist[command][1]
        embede = discord.Embed(title=commandtitle,description=commandsdesc,colour=0xF7B755)
        await ctx.send(embed=embede)
"""

class generalcommands():

    def __init__(self):
        pass

    async def commands(self,ctx,category=None):
            if category == None:
                    embede = discord.Embed(title="Command categories:",description="General\nSpotify\nGenius\nReddit\nPlayer\nAzure\nTrash")
                    await ctx.send(embed=embede)
            else:
                    commandir = {
    "General":{
            "ping":"<>",
            "commands":"<category>",
            "good":"<>",
            "bad":"<>",
            "nuke":"<channel>",
            "kick":"<user> <origin>",
            "roll":"<upper bound>",
            "embed":"<title> <description> <url> <imageurl>"},
    "Spotify":{
            "playlists":"<user>",
            "artistalbums":"<artist>",
            "artistinfo":"<artist>",
            "tracklist":"<album>",
            "trackinfo":"<track>",
            "toptracks":"<artist>"},
    "Genius":{
            "lyrics":"<track>"},
    "Reddit":{
            "topcomment":"<user>",
            "bottomcomment":"<user>",
            "toppost":"<subreddit> <timescale>",
            "randomsub":"<>",
            "randnsfw":"<>"},
    "Player":{
            "qadd":"<query or URL>",
            "qsub":"<place>",
            "q":"<>",
            "playq":"<channel>",
            "skip":"<>",
            "pause":"<>",
            "resume":"<>",
            "clear":"<>",
            "resume":"<>",
            "dc":"<>"},
    "Azure":{
            "identify":"<imageurl>",
            "define":"<word>",
            "img":"<query> <number>"},
    "Trash":{
            "pong":"<>",
            "alexa":"<a> <b>",
            "dame":"<a> <b>",
            "this":"<a> <b> <c>",
            "embedtest":"<>",
            "game":"<>",
            "qplay":"<>"}
    }
                    if category in commandir:
                            msg = ""
                            for i in commandir[category]:
                                    msg = msg + i + " " + commandir[category][i] + "\n"
                            embede = discord.Embed(title=("Commands in category: "+category),description=msg,colour=0xF7B755)
                            await ctx.send(embed=embede)
                    else:
                            embede = discord.Embed(title="Command categories:",description="General\nSpotify\nGenius\nReddit\nPlayer\nAzure\nTrash")
                            await ctx.send(embed=embede)



    #returns a smiling emote
    # Fix on missing bot
    async def good(self,ctx,bot):
            if bot == "bot":
                    await ctx.send("<:curtaincall:448219599587115019>")

    #returns a sad emote
    #fix on missing bot param
    async def bad(self,ctx,bot):
            if bot == "bot":
                    await ctx.send("<:TrampolineVirgin:448217952311967764>")

    async def ping(self,ctx):
        await ctx.send(":ping_pong: Pong!")

    async def hello(self,ctx):
        await ctx.send("Hi {}!".format(ctx.author))

    async def nuke(self,ctx,destination="429574068224786433"):
        #chubid = "427895499560058895"
        #barracudaid = "429563110102138880"
        #pikeid = "429563098161086475"
        destinationTO = "429574068224786433"
        try:
                voice_channel = discord.utils.get(ctx.message.server.channels, name=destination, type=discord.ChannelType.voice)
        except:
                return None
        members = voice_channel.voice_members
        memids = []
        if destination == "Chub":
            destinationFrom = '427895499560058895'
        elif destination == "Barracuda":
            destinationFrom = '429563110102138880'
        elif destination == "Pike":
            destinationFrom = '429563098161086475'
        else:
            destinationFrom = '429574068224786433'
        for member in members:
                memids.append(member.id)
        print(memids)
        for i in memids:
                await client.move_member(ctx.message.server.get_member(i), client.get_channel(destinationTO))
        await client.edit_channel(client.get_channel(destinationFrom),bitrate=8000)
        embede = discord.Embed(colour=0xFF0055)
        embede.set_image(url="https://memegenerator.net/img/images/16331463/elmo-nuke.jpg")
        await ctx.send(embed=embede)
        await asyncio.sleep(10)
        await client.edit_channel(client.get_channel(destinationFrom),bitrate=16000)
        await asyncio.sleep(10)
        await client.edit_channel(client.get_channel(destinationFrom),bitrate=32000)
        await asyncio.sleep(10)
        await client.edit_channel(client.get_channel(destinationFrom),bitrate=64000)


    #Moves a user to a new channel then dletes the channel, disconnectin gthem from voice
    #Does not work
    async def kick(self,ctx,username="samplename",channelfrom="Pike"):
        try:
            voice_channel_from = discord.utils.get(ctx.message.server.channels, name=channelfrom, type=discord.ChannelType.voice)
        except:
            return None
        if voice_channel_from == None:
                return None
        else:
                members = voice_channel_from.voice_members
                for member in members:
                        if member.name == username:
                                await client.create_channel(ctx.message.server, "Kicktemp", type=discord.ChannelType.voice)
                                await asyncio.sleep(0.5)
                                voice_channel_to = discord.utils.get(ctx.message.server.channels, name="Kicktemp", type=discord.ChannelType.voice)
                                await asyncio.sleep(0.5)
                                await client.move_member(member,voice_channel_to)
                                await asyncio.sleep(0.5)
                                await client.delete_channel(voice_channel_to)
                                await ctx.send(":boot:")


    #rolls a random number between 1 and the given upper bound
    async def roll(self,ctx,upperbound):
            try:
                    upperbound = int(upperbound)
            except:
                    await ctx.send("Enter an integer above 1")
                    return
            if upperbound < 2:
                    await ctx.send("Enter an integer above 1")
                    return
            rang = "(1-" + str(upperbound) +")"
            result = str(random.randrange(1,upperbound+1))
            embede = discord.Embed(title=result,description=rang,colour=0xF7B755)
            await ctx.send(embed=embede)




    #reference for my embeds
    #@client.command()
    #async def embedtest():
    #      embede = discord.Embed(title="Title",description="description",colour=0xF7B755)
    #      embede.set_footer(text="Footer")
    #      await ctx.send(embed=embede)

    #allows the user to embed something (as users cannot do embeds) and deletes the message that called this command.
    #Fix errors on trying to delete previous message
    async def embed(self,ctx,title_in=None,description_in=None,url_in=None,imageurl_in=None):
            deets = [title_in,description_in,url_in,imageurl_in]
            if all(y == None for y in deets):
                    embede = discord.Embed(title="Syntax",description="Title, description, url, imageurl \n x for blank",colour=0xF7B755) #This gives some syntax help if they leave all fields blank
                    await ctx.send(embed=embede)
            else:
                    try:
                            for z in deets:
                                    if z == "x":
                                            deets[deets.index(z)] = None #changes al blank fields into actual blank feilds
                            embede = discord.Embed(title=deets[0],description=deets[1],url=deets[2],colour=0xFFFFFF)
                            if deets[3] != None:
                                    embede.set_image(url=deets[3])
                            await ctx.send(embed=embede)
                    except:
                            embede = discord.Embed(title="Error",colour=0xF7B755)
                            await ctx.send(embed=embede)
            await client.delete_message(ctx.message)  #deletes the message
