import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import platform
import requests
import requests.auth
import spotipy
import spotipy.util as util


# Here you can modify the bot's prefix and description and wether it sends help in direct messages or not.
client = Bot(description="back,sack,crackBot", command_prefix="¬", pm_help = False)

#spotify colour : 0x1F7A1F
# reddit colur: 0xFF0055
# genius colour: 0xFFFF66
# defualt coliur: 0xF7B755
#yoo toob colour 0x3DE5C3

#######################################################################

def key_setup():
    keydict = {}
    keyfile = open(".keys.txt","r")
    keylines = [line.split() for line in keyfile.readlines()]

    keydict['redditkey1'] = keylines[1][1]
    keydict['redditkey2'] = keylines[2][1]
    keydict['redditpass'] = keylines[3][1]
    keydict['spotifykey1'] = keylines[6][1]
    keydict['spotifykey2'] = keylines[7][1]
    keydict['geniussecret'] = keylines[10][1]
    keydict['geniusid'] = keylines[11][1]
    keydict['geniusaccess'] = keylines[12][1]
    keydict['finalkey'] = keylines[15][1]
    keydict['subscription_key'] = keylines[16][1]
    keydict['subscription_key1'] = keylines[17][1]
    keydict['token'] = util.prompt_for_user_token(username="doleary2k",scope="user-library-read",client_id=keydict['spotifykey1'],client_secret=keydict['spotifykey2'],redirect_uri='http://mysite.com/callback/')

    keyfile.close()

    return keydict
keydict = key_setup()

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



#returns the bing definition of a specified word
## Does not work, API key error
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
# Does not work
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
########################################################################################
import redditcommands
reddit_module = redditcommands.redditcommands("redditkey1","redditkey2","redditpass")

@client.command()
async def bottomcomment(ctx,user): await reddit_module.bottomcomment(ctx,user)

@client.command()
async def topcomment(ctx,user): await reddit_module.topcomment(ctx,user)

@client.command()
async def toppost(ctx,subreddit,period="all"): await reddit_module.toppost(ctx,subreddit,period="all")

@client.command()
async def randomsub(ctx): await reddit_module.randomsub(ctx)

#######################################################################################
##################### GENERAL STUFF
#######################################################################################
import generalcommands
general_module = generalcommands.generalcommands()

@client.command()
async def ping(ctx): await general_module.ping(ctx)

@client.command()
async def hello(ctx): await general_module.hello(ctx)

@client.command()
async def commands(ctx,category=None): await general_module.commands(ctx,category=None)

@client.command()
async def good(ctx,bot): await general_module.good(ctx,bot)

@client.command()
async def bad(ctx,bot): await general_module.bad(ctx,bot)

@client.command()
async def nuke(ctx,destination="429574068224786433"): await general_module.nuke(ctx,destination="429574068224786433")

@client.command()
async def kick(ctx,username="samplename",channelfrom="Pike"): await general_module.kick(ctx,username="samplename",channelfrom="Pike")

@client.command()
async def roll(ctx,upperbound): await general_module.roll(ctx,upperbound)

@client.command()
async def embed(ctx,title_in=None,description_in=None,url_in=None,imageurl_in=None): await general_module.embed(ctx,title_in=None,description_in=None,url_in=None,imageurl_in=None)

#######################################################################################
##################### SPOTIFY STUFF
#######################################################################################
import spotifycommands
spotify_module = spotifycommands.spotifycommands(keydict['token'])

@client.command()
async def playlists(ctx,username):  await spotify_module.playlists(ctx,username)

@client.command()
async def artistalbums(ctx,artist): await spotify_module.artistalbums(ctx,artist)

@client.command()
async def artistinfo(ctx,artist): await spotify_module.artistinfo(ctx,artist)

@client.command()
async def tracklist(ctx,album): await spotify_module.tracklist(ctx,album)

@client.command()
async def trackinfo(ctx,track): await spotify_module.trackinfo(ctx,track)

@client.command()
async def toptracks(ctx,artist): await spotify_module.toptracks(ctx,artist)

#######################################################################################
##################### GENIUS STUFF
#######################################################################################
import geniuscommands
genius_module = geniuscommands.geniuscommands()

@client.command()
async def lyrics(ctx,trackname="Despacito"): await genius_module.lyrics(ctx,trackname="Despacito")

#######################################################################################
##################### PLAYER SUFF
#######################################################################################
import playercommands
player_module = playercommands.playercommands()

@client.command(pass_context = True)
async def dc(ctx): await player_module.dc(ctx)

@client.command()
async def clear(ctx): await player_module.clear(ctx)

@client.command(pass_context = True)
async def pause(ctx): await player_module.pause(ctx)

@client.command(pass_context = True)
async def resume(ctx): await player_module.resume(ctx)

@client.command(pass_context=True)
async def q(ctx): await player_module.q(ctx)

@client.command(pass_context=True)
async def qadd(ctx): await player_module.qadd(ctx)

@client.command()
async def qsub(ctx,place=None): await player_module.qsub(ctx,place=None)

@client.command(pass_context=True)
async def playq(ctx,channel="ohgodmykeeb"): await player_module.playq(ctx,channel="ohgodmykeeb")

@client.command()
async def qplay(ctx): await player_module.qplay(ctx)

@client.command()
async def skip(ctx): await player_module.skip(ctx)

################################


client.run(keydict['finalkey'])

# Basic Bot template was created by Habchy#1665
# Adapted and built upon by Sudocrèm#2245
