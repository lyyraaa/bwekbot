import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import platform
import requests
import requests.auth
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib import patches
from io import BytesIO
from pprint import pprint
import json
import time
import random
import spotipy
import spotipy.util as util
import sys
import os
import math
import lyricsgenius as genius
import youtube_dl
import subprocess
import urllib.request
from bs4 import BeautifulSoup

# Here you can modify the bot's prefix and description and wether it sends help in direct messages or not.
client = Bot(description="back,sack,crackBot", command_prefix="¬", pm_help = False)




#spotify colour : 0x1F7A1F
# reddit colur: 0xFF0055
# genius colour: 0xFFFF66
# defualt coliur: 0xF7B755
#yoo toob colour 0x3DE5C3

#######################################################################


def key_setup():
    keyfile = open(".keys.txt","r")
    keylines = [line.split() for line in keyfile.readlines()]

    global redditkey1
    redditkey1 = keylines[1][1]
    global redditkey2
    redditkey2 = keylines[2][1]
    global redditpass
    redditpass = keylines[3][1]
    global spotifykey1
    spotifykey1 = keylines[6][1]
    global spotifykey2
    spotifykey2 = keylines[7][1]
    global geniussecret
    geniussecret = keylines[10][1]
    global geniusid
    geniusid = keylines[11][1]
    global geniusaccess
    geniusaccess = keylines[12][1]
    global finalkey
    finalkey = keylines[15][1]
    global subscription_key
    subscription_key = keylines[16][1]
    global subscription_key1
    subscription_key1 = keylines[17][1]

    global token
    token = util.prompt_for_user_token(username="doleary2k",scope="user-library-read",client_id=spotifykey1,client_secret=spotifykey2,redirect_uri='http://mysite.com/callback/')

    keyfile.close()

#Does the stuff to initialise the bot
@client.event
async def on_ready():
    #print('Logged in as '+client.user.name+' (ID:'+client.user.id+') | Connected to '+str(len(client.servers))+' servers | Connected to '+str(len(set(client.get_all_members())))+' users')
    print('--------')
    print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))
    print('--------')
    print('Use this link to invite {}:'.format(client.user.name))
    print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(client.user.id))
    print('--------')
    print('Support Discord Server: https://discord.gg/FNNNgqb')
    print('Github Link: https://github.com/Habchy/BasicBot')
    print('--------')
    print('You are running BasicBot v2.1') #Do not change this. This will really help us support you, if you need support.
    #return await client.change_presence(game=discord.Game(name='Rigby Dillum')) #This is buggy, let us know if it doesn't work.




# This is a basic example of a call and response command. You tell it do "this" and it does it.
@client.command()
async def ping(ctx):
    await ctx.send(":ping_pong: Pong!")

@client.command()
async def hello(ctx):
    await ctx.send("Hi {}!".format(ctx.author))


#returns the bing definition of a specified word
@client.command()
async def define(ctx,word=""):
        if word == "": return
        search_term = "define "+str(word)
        search_url = "https://api.cognitive.microsoft.com/bing/v7.0/search"
        headers = {"Ocp-Apim-Subscription-Key" : subscription_key1}
        params  = {"q": search_term, "textDecorations":True, "textFormat":"HTML"}
        response = requests.get(search_url, headers=headers, params=params)
        response.raise_for_status()
        search_results = response.json()
        pages = search_results["webPages"]
        result = search_results["webPages"]["value"][3]["snippet"]
        result = result.replace("<b>","")
        result = result.replace("</b>","")
        await ctx.send(result)



#returns the corresponding image result for a specified term from bing images

@client.command()
async def img(ctx,searchterm,resultnumber):
        try:
                int(resultnumber) % 1
        except:
                await ctx.send("Enter an integer")
                return
        if int(resultnumber) > 10:
                await ctx.send("Keep it under 10")
                return
        elif int(resultnumber) < 1:
                await ctx.send("Keep it above 0")
                return
        search_term = str(searchterm)
        search_url = "https://api.cognitive.microsoft.com/bing/v7.0/images/search"
        headers = {"Ocp-Apim-Subscription-Key" : subscription_key1}
        params  = {"q": search_term, "license": "public", "imageType": "photo", "isFamilyFriendly": False}
        response = requests.get(search_url, headers=headers, params=params)
        response.raise_for_status()
        search_results = response.json()
        thumbnail_urls = [img["thumbnailUrl"] for img in search_results["value"][(int(resultnumber)-1):int(resultnumber)]]
        if not thumbnail_urls:
                await ctx.send("No results found")
        else:
                await ctx.send(thumbnail_urls[0])



#######################################################################################
##################### REDDIT STUFF
#######################################################################################


@client.command()
async def bottomcomment(ctx,user):
        client_auth = requests.auth.HTTPBasicAuth(redditkey1,redditkey2)
        post_data = {"grant_type": "password", "username": "KnackBot", "password": redditpass}
        headers = {"User-Agent": "KnackBot"}
        resp = requests.get("https://www.reddit.com/user/"+user+"/comments/.json?sort=controversial&?t=all", headers = {'User-agent': 'KnackBot'})
        respo = resp.json()
        try:
                authorscore = str(respo["data"]["children"][0]["data"]["author"]) + "  |  Score:  " + str(respo["data"]["children"][0]["data"]["score"])
                body = (respo["data"]["children"][0]["data"]["body"])
                embede = discord.Embed(title=authorscore,description=body,colour=0xFF0055)
                await ctx.send(embed=embede)
        except:
                await ctx.send("Error")




@client.command()
async def topcomment(ctx,user):
        client_auth = requests.auth.HTTPBasicAuth(redditkey1,redditkey2)
        post_data = {"grant_type": "password", "username": "KnackBot", "password": redditpass}
        headers = {"User-Agent": "KnackBot by Yeety"}
        resp = requests.get("https://www.reddit.com/user/"+user+"/comments/.json?sort=top&?t=all", headers = {'User-agent': 'KnackBot'})
        respo = resp.json()
        try:
                authorscore = str(respo["data"]["children"][0]["data"]["author"]) + "  |  Score:  " + str(respo["data"]["children"][0]["data"]["score"])
                body = (respo["data"]["children"][0]["data"]["body"])
                embede = discord.Embed(title=authorscore,description=body,colour=0xFF0055)
                await ctx.send(embed=embede)
        except:
                await ctx.send("Error")


#returns the current top post from a given subreddit it a given time period. Returns the tital, score and link (if there is one)
@client.command()
async def toppost(ctx,subreddit,period="all"):
        if period not in ("day","week","month","year","all"):
                await ctx.send("Parameters for top: day, week, month, year, all")
                return
        try:
                client_auth = requests.auth.HTTPBasicAuth(redditkey1,redditkey2)
                post_data = {"grant_type": "password", "username": "KnackBot", "password": redditpass}
                headers = {"User-Agent": "KnackBot by Yeety"}
                resp = requests.get("https://www.reddit.com/r/"+subreddit+"/top/.json?t="+period, headers = {'User-agent': 'KnackBot'})
                respo = resp.json()
                subredditscore = ("Subreddit:   " + respo["data"]["children"][0]["data"]["subreddit"]) + "  |  " + ("Score:   " + str(respo["data"]["children"][0]["data"]["score"]))
                titlepost = (respo["data"]["children"][0]["data"]["title"])
                posturl = (respo["data"]["children"][0]["data"]["url"])
                try:
                        imageurl = (respo["data"]["children"][0]["data"]["preview"]["images"][0]["source"]["url"])
                        flag = True
                except:
                        flag = False
                if flag == True:
                        embede = discord.Embed(title=subredditscore,description=titlepost,url=posturl,colour=0xFF0055)
                        embede.set_image(url=imageurl)
                        await ctx.send(embed=embede)
                elif flag == False:
                        embede = discord.Embed(title=subredditscore,description=titlepost,url=posturl,colour=0xFF0055)
                        await ctx.send(embed=embede)
        except:
                await ctx.send("Error")


#returns the top post in a random subreddit
@client.command()
async def randomsub(ctx):
        try:
                client_auth = requests.auth.HTTPBasicAuth(redditkey1,redditkey2)
                post_data = {"grant_type": "password", "username": "KnackBot", "password": redditpass}
                headers = {"User-Agent": "KnackBot by Yeety"}
                response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
                responses = response.json()
                resp = requests.get("https://www.reddit.com/r/random/top/.json?t=all", headers = {'User-agent': 'KnackBot'})
                respo = resp.json()
                subredditscore = ("Subreddit:   " + respo["data"]["children"][0]["data"]["subreddit"]) + "  |  " + ("Score:   " + str(respo["data"]["children"][0]["data"]["score"]))
                titlepost = (respo["data"]["children"][0]["data"]["title"])
                posturl = (respo["data"]["children"][0]["data"]["url"])
                try:
                        imageurl = (respo["data"]["children"][0]["data"]["preview"]["images"][0]["source"]["url"])
                        flag = True
                except:
                        flag = False
                if flag == True:
                        embede = discord.Embed(title=subredditscore,description=titlepost,url=posturl,colour=0xFF0055)
                        embede.set_image(url=imageurl)
                        await ctx.send(embed=embede)
                elif flag == False:
                        embede = discord.Embed(title=subredditscore,description=titlepost,url=posturl,colour=0xFF0055)
                        await ctx.send(embed=embede)
        except:
                await ctx.send("Error")

#######################################################################################
##################### GENERAL STUFF
#######################################################################################

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


@client.command()
async def commands(ctx,category=None):
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
@client.command()
async def good(ctx,bot):
        if bot == "bot":
                await ctx.send("<:curtaincall:448219599587115019>")

#returns a sad emote
@client.command()
async def bad(ctx,bot):
        if bot == "bot":
                await ctx.send("<:TrampolineVirgin:448217952311967764>")



#moves all users from a given channel into the afk channel, then destroys the bitrate of that channel, it exponentially recovers over 30 seconds
@client.command(pass_context=True)
async def nuke(ctx,destination="429574068224786433"):
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
@client.command(pass_context=True)
async def kick(ctx,username="samplename",channelfrom="Pike"):
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
@client.command()
async def roll(ctx,upperbound):
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
@client.command(pass_context=True)
async def embed(ctx,title_in=None,description_in=None,url_in=None,imageurl_in=None):
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


#######################################################################################
##################### SPOTIFY STUFF
#######################################################################################

#final level command, shows all playlists and song count for given user.
@client.command()
async def playlists(ctx,username):
    if token:
        sp = spotipy.Spotify(auth=token)
        playlists = sp.user_playlists(username)
        playlisttitle = ("Public playlists for "+ username + "\n")
        content = ""
        for playlist in playlists['items']:
            if playlist['owner']['id'] == username:
                content = content + (playlist['name']+"  -  "+ str(playlist['tracks']['total']) + " tracks \n")
        embede = discord.Embed(title=playlisttitle,description=content,colour=0x1F7A1F)
        await ctx.send(embed=embede)
    else:
        await ctx.send("Can't get token for"+ username)



async def get_artist(ctx,name):
    results = sp.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        return items[0]
    else:
        return None


async def show_artist_albums(ctx,artist):
    albums = []
    output = []
    results = sp.artist_albums(artist['id'], album_type='album')
    albums.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        albums.extend(results['items'])
    seen = set() # to avoid dups
    for album in albums:
        name = album['name']
        if name not in seen:
            output.append(name)
            seen.add(name)
    return output


async def get_album(ctx,album):
    results = sp.search(q='album:' + album, type='album')
    items = results['albums']['items']
    albumid = items[0]["id"]
    albumurl = items[0]["external_urls"]["spotify"]
    albumcoverurl = items[0]["images"][0]["url"]
    if len(items) > 0:
        return(albumid,albumurl,albumcoverurl)
    else:
        return None


async def get_track(ctx,track):
    results = sp.search(q='track:' + track, type='track')
    items = results['tracks']['items']
    trackpopularity = items[0]["popularity"]
    trackurl = items[0]["external_urls"]["spotify"]
    trackid = items[0]["id"]
    trackruntime = int(items[0]["duration_ms"])/1000
    runtimesecs = math.floor(trackruntime%60)
    runtimemin = math.floor(trackruntime/60)
    trackruntime = str(runtimemin)+":"+str(runtimesecs)
    trackexplicit = items[0]["explicit"]
    if len(items) > 0:
        return(trackpopularity,trackurl,trackruntime,trackexplicit,trackid)
    else:
        return None


async def gettoptracks(ctx,artistid):
    tracks = []
    results = sp.artist_top_tracks(ctx,artistid)
    for x in range(5):
        trackalbumname = (results["tracks"][x]["album"]["name"])
        trackname = (results["tracks"][x]["name"])
        output = trackname + "  -  " + trackalbumname
        tracks.append(output)
    return(tracks)

#final level command, shows all albums of given artist
@client.command()
async def artistalbums(ctx,artist):
    artist = await get_artist(ctx,artist)
    if artist:
        out = await show_artist_albums(ctx,artist)
        artistalbumtitle = "Albums by " + str(artist["name"])
        output = ""
        for i in out:
            output = output + str(i) + "\n"
        embede = discord.Embed(title=artistalbumtitle,description=output,colour=0x1F7A1F)
        await ctx.send(embed=embede)
    else:
        await ctx.send("Can't find that artist")


#final level command, shows a few things about an artis lie pic, followers, genre
@client.command()
async def artistinfo(ctx,artist):
    artist = await get_artist(ctx,artist)
    if artist:
        titleartist = ('===='+ artist['name']+ '====')
        imageurl = (artist["images"][1]["url"])
        followers = ('Followers: '+ str(artist['followers']["total"])+ "\n")
        if len(artist['genres']) > 0:
            followers = followers + ('Genres: '+ ','.join(artist['genres']))
        embede = discord.Embed(title=titleartist,description=followers,colour=0x1F7A1F)
        embede.set_image(url=imageurl)
        await ctx.send(embed=embede)

##final level command, shows tracklist of given album
@client.command()
async def tracklist(ctx,album):
    album = await get_album(album)
    if album:
        await ctx.send(album[1])

#final level command, shows track and explicity, populaeiryt and r4ubntiem.
@client.command()
async def trackinfo(ctx,track):
    track = await get_track(track)
    if track:
        await ctx.send(track[1])
        #print(track[4])
        descrip = "Explicit: "+str(track[3])+"  |  Popularity: "+str(track[0])+"  |  Duration: "+str(track[2])
        embede = discord.Embed(description=descrip,colour=0x1F7A1F)
        await ctx.send(embed=embede)

#final level command, gets the tp 5 tracks for any artist
@client.command()
async def toptracks(ctx,artist):
    artist = await get_artist(artist)
    if artist:
        artistid = artist["id"]
        top5title = ("Top 5 from "+ artist["name"])
        out = await gettoptracks(artistid)
        outputdesc = ""
        for i in out:
            outputdesc = outputdesc + i + "\n"
        embede = discord.Embed(title=top5title,description=outputdesc,colour=0x1F7A1F)
        await ctx.send(embed=embede)

#######################################################################################
##################### GENIUS STUFF
#######################################################################################

#gets the lyrics from genius for a given song, is forced to split it up into multiple messages if it exceeds discords built in llimit of 2k chars
@client.command()
async def lyrics(ctx,trackname="Despacito"):
        if trackname == "Despacito":
                embede = discord.Embed(title="Please input track title",colour=0xFFFF66)
                return
        api = genius.Genius("geniusaccess")
        lyricstitle = "Result for: '"+trackname+"'"
        lyricsdesc = (api.search_song(trackname).__dict__)["_body"]["lyrics"]
        lyriclength = len(lyricsdesc)
        lowerpointer = 0
        upperpointer = 2000
        embede = discord.Embed(title=lyricstitle,colour=0xFFFF66)
        await ctx.send(embed=embede)
        if lyriclength > 2000:
                while lowerpointer < lyriclength:
                        await ctx.send(lyricsdesc[lowerpointer:upperpointer])
                        lowerpointer += 2000
                        upperpointer += 2000
        else:
                await ctx.send(lyricsdesc)


#######################################################################################
##################### PLAYER SUFF
#######################################################################################
global player
global playqueue
global isvoiceconnected
global voice
isvoiceconnected = False
playqueue = []
player = False
#Im too bad at coding to have these be passed between functions and Im not even sure it cna be done so here they are as global vars



#connects to a voice channel is not already connected
async def connectto(ctx,channel):
        global isvoiceconnected
        global voice
        if isvoiceconnected == True:
                return("Already connected")
        elif channel not in ["Chub","Pike","Barracuda"]:
                return("Invalid channel")
        else:
              voice_channel_to = discord.utils.get(ctx.message.server.channels, name=channel, type=discord.ChannelType.voice)
              voice = await client.join_voice_channel(voice_channel_to)
              isvoiceconnected = True

#disconnects from every voice channel and wipes the queue. This is a hard dc and if this bot ran on multiple servers, it would disconnect from all of them
@client.command(pass_context = True)
async def dc(ctx):
    global playqueue
    global player
    playqueue = []
    global isvoiceconnected
    if isvoiceconnected == False:
            embede = discord.Embed(title="Not connected",colour=0x3DE5C3)
            await ctx.send(embed=embede)
    else:
            isvoiceconnected = False
            for x in client.voice_clients:
                return await x.disconnect()

#clears the queue but doesnt dc
@client.command()
async def clear(ctx,):
        global playqueue
        playqueue = []
        embede = discord.Embed(title="Queue cleared",colour=0x3DE5C3)
        await ctx.send(embed=embede)


#starts the player for a given url
async def startplayer(url):
        global isvoiceconnected
        global voice
        global player
        if isvoiceconnected == False:
                print("Not connected to voice")
                return
        else:
              try:
                      player = await voice.create_ytdl_player(url)
                      player.start()
              except:
                      print("Error in creating or starting voice")

#Unused but will return true once the player finishes the current tjing
async def checkdone():
        global player
        while player.is_done() == False:
                await asyncio.sleep(1)
        return True

#Like the last one, but for this specific one it will advance the queue and then play the next thing
async def checkdone_q(ctx,channel):
        global player
        while player.is_done() == False:
                await asyncio.sleep(1)
        print("Finished")
        await qsubtract(1,False)
        await asyncio.sleep(1)
        try:
                await play_queue(ctx,channel)
        except:
                print("Queue ended unknown")

#is the player is playing, it pauses it
@client.command(pass_context = True)
async def pause(ctx):
        global isvoiceconnected
        global player
        if isvoiceconnected == False:
                embede = discord.Embed(title="Not connected",colour=0x3DE5C3)
                await ctx.send(embed=embede)
        else:
                cond = player.is_playing()
                if cond == True:
                        player.pause()
                        embede = discord.Embed(title="Player paused",colour=0x3DE5C3)
                        await ctx.send(embed=embede)
                else:
                        embede = discord.Embed(title="Not playing",colour=0x3DE5C3)
                        await ctx.send(embed=embede)


#if the player is paused, it resumes it
@client.command(pass_context = True)
async def resume(ctx):
        global player
        global isvoiceconnected
        if isvoiceconnected == False:
                embede = discord.Embed(title="Not connected",colour=0x3DE5C3)
                await ctx.send(embed=embede)
        else:
                cond = player.is_done()
                if cond == False:
                        player.resume()
                        embede = discord.Embed(title="Player resumed",colour=0x3DE5C3)
                        await ctx.send(embed=embede)
                else:
                        embede = discord.Embed(title="Player done",colour=0x3DE5C3)
                        await ctx.send(embed=embede)

#Gets some information on the url it is given. It has to load the video first so this is used for thing sthat dont need to be fast, and not in the queue print
async def getviddeets(url="url"):
        if url == "url":
                print("no url given")
        else:
                ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'}) #Crikey I dont know how this works
                with ydl:
                    try:
                        result = ydl.extract_info(url,download=False)
                    except:
                            print("error searching URL")
                if 'entries' in result:
                    video = result['entries'][0]
                else:
                    video = result
                vid_title = (video["title"])
                vid_duration = (video["duration"])
                try:
                        vid_thumbnail = (video["thumbnail"])[:len(video["thumbnail"])-4]
                except:
                        vid_thumbnail = "https://i.ytimg.com/vi/b8HO6hba9ZE/hqdefault.jpg%27" #Just a placeholder if the thumbnail doesnt work
                return(vid_title,vid_duration,vid_thumbnail)
        return None


#i failed you sensei, I stole this from some guy on stack overflow because youtube-dl has trash documentation. at least i modified it and correctly spelled response i guess
#As a result, this searches in a completely different way to the URL pure search, this scrapes the HTML and gets the URL and titles of all the videos.
async def term_to_url(searchterm="wheatthings"):
        if searchterm == "wheatthings":
                print("No term given")
        else:
                searchstring = searchterm.replace
                response = urllib.request.urlopen('https://www.youtube.com/results?search_query='+searchterm)
                soup = BeautifulSoup(response, "html.parser")
                divs = soup.find_all("div", { "class" : "yt-lockup-content"}) #This gets allt he results on the first page from the div classes that hold the videos.
                href = divs[0].find('a', href=True) #This bit gets the information with the link (<a>) tag of the first result
                video_title = href.text
                video_url = "https://www.youtube.com"+href['href']
                return(video_title,video_url)

#Displays the Queue
@client.command(pass_context=True)
async def q(ctx):
        count = 1
        if playqueue == []:
                embede = discord.Embed(title="Error",description="Queue empty",colour=0x3DE5C3)
                await ctx.send(embed=embede)
        else:
                q_mess = ""
                for x in playqueue:
                        q_mess = q_mess + (str(count)+"  |  "+ str(playqueue[count-1][1])+ "\n")
                        count += 1
                embede = discord.Embed(title="Queue:",description=q_mess,colour=0x3DE5C3)
                await ctx.send(embed=embede)

#adds an item to teh queue, not a command so can be called
async def qaddition(url_in="blankisole"):
        if url_in == "blankisole":
                embede = discord.Embed(title="Error",description="Please enter a URL or search term",colour=0x3DE5C3)
                await ctx.send(embed=embede)
                return
        url_in = url_in.replace(" ","%20")
        if "http" not in url_in:
                out = await term_to_url(url_in)
                url = out[1]
                vid_title = out[0]
        else:
                out = await term_to_url(url_in)
                url = url_in
                vid_title = out[0]
        if "channel" in url or "user" in url:
                embede = discord.Embed(title="First result was a channel",description="Try being more specific",colour=0x3DE5C3)
                await ctx.send(embed=embede)
                return
        if len(playqueue) < 10:
                playqueue.append([url,vid_title])
                success_mess = "Sucessfully added: <" +vid_title+">"
                embede = discord.Embed(description=success_mess,colour=0x3DE5C3)
                await ctx.send(embed=embede)
        else:
                embede = discord.Embed(title="Queue full",colour=0x3DE5C3)
                await ctx.send(embed=embede)

#adds 2 q
@client.command(pass_context=True)
async def qadd(ctx):
        data = ctx.message.content
        data = data[6:]
        if len(data) == 0:
                embede = discord.Embed(title="Error",description="Please enter a URL or search term",colour=0x3DE5C3)
                await ctx.send(embed=embede)
        else:
                await qaddition(data)



#same situation as addition, this one needs to be called elsewhere to cannot be a client command
async def qsubtract(place=-1,doprint=False):
        try:
                place = int(place)
        except:
                embede = discord.Embed(title="Error",description="Invalid place",colour=0x3DE5C3)
                await ctx.send(embed=embede)
                return
        if place < 1 or place > len(playqueue):
                embede = discord.Embed(title="Error",description="Invalid place",colour=0x3DE5C3)
                await ctx.send(embed=embede)
        else:
                if doprint == True:
                        success_mess = ("Successfully removed: <" +playqueue[place-1][1]+">")
                        embede = discord.Embed(description=success_mess,colour=0x3DE5C3)
                        await ctx.send(embed=embede)
                playqueue.remove(playqueue[place-1])

#yeet
@client.command()
async def qsub(ctx,place=None):
        await qsubtract(place,True)


#This starts playing the queue in the given voice channel
@client.command(pass_context=True)
async def playq(ctx,channel="ohgodmykeeb"):
        global player
        global isvoiceconnected
        if channel not in ["Chub","Barracuda","Pike"]:
                #await ctx.send("Invalid channel")
                embede = discord.Embed(title="Error",description="Invalid channel",colour=0x3DE5C3)
                await ctx.send(embed=embede)
                return
        if isvoiceconnected == True:
                isdone = False
                try:
                        isdone = player.is_done()
                except:
                        ""
                if isdone == False:
                        embede = discord.Embed(title="Already playing",colour=0x3DE5C3)
                        await ctx.send(embed=embede)
                else:
                        await play_queue(ctx,channel)
        else:
                await play_queue(ctx,channel)

#people keep gettn them mixed up smdh
@client.command()
async def qplay(ctx):
        await ctx.send("did you mean playq?")

#THis is the callable function that starts playing the queue, it calls the other functions to start up the player and connect if it has not already.
async def play_queue(ctx,channel="Nyetcomrade"):
        if channel == "Nyetcomrade":
                print("Error with connecting to channel")
        global player
        global playqueue
        global isvoiceconnected
        global voice
        if isvoiceconnected == False:
                await connectto(ctx,channel)
        if len(playqueue) < 1:
                #await ctx.send("Queue empty")
                embede = discord.Embed(title="Queue empty",colour=0x3DE5C3)
                await ctx.send(embed=embede)
        else:
                await startplayer(playqueue[0][0])
                asyncio.ensure_future(checkdone_q(ctx,channel))
                return


#skips currently playing by termninatiing the ytdl stream. Luckily this works really well with the checkdone q function, as that will automatically start playing the next thhing in the right channel
@client.command()
async def skip(ctx):
        global player
        global isvoiceconnected
        global playqueue
        if isvoiceconnected == False:
                embede = discord.Embed(title="Not connected to voice",colour=0x3DE5C3)
                await ctx.send(embed=embede)
                return
        isdone = False
        try:
                isdone = player.is_done()
        except:
                ""
        if isdone == True:
                embede = discord.Embed(title="Player done",colour=0x3DE5C3)
                await ctx.send(embed=embede)
                return
        else:
                embede = discord.Embed(title="Skipped",description=playqueue[0][1],colour=0x3DE5C3)
                await ctx.send(embed=embede)
                player.resume() #If the player is paused then stopped it will "stop" the player and it cant be resumed but it leaves a window open and uses memory. If it is resumed first it is a cleaner cut and ffmpeg closes correctly
                player.stop()



################################

key_setup()
client.run(finalkey)

# Basic Bot template was created by Habchy#1665
# Adapted and built upon by Sudocrèm#2245
