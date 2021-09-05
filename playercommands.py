import asyncio
import discord
from discord.ext.commands import Bot
from discord.ext import commands
import os
import youtube_dl
import urllib.request
from bs4 import BeautifulSoup

class playercommands():

    def __init__(self):
        self.player = False
        self.playqueue = []
        self.isvoiceconnected = False
        self.voice = None

    #connects to a voice channel is not already connected
    async def connectto(self,ctx,channel):
            if self.isvoiceconnected:
                    return("Already connected")
            elif channel not in ["Chub","Pike","Barracuda"]:
                    return("Invalid channel")
            else:
                  voice_channel_to = discord.utils.get(ctx.message.server.channels, name=channel, type=discord.ChannelType.voice)
                  self.voice = await client.join_voice_channel(voice_channel_to)
                  self.isvoiceconnected = True

    #disconnects from every voice channel and wipes the queue. This is a hard dc and if this bot ran on multiple servers, it would disconnect from all of them
    async def dc(self,ctx):
        self.playqueue = []
        if not self.isvoiceconnected:
                embede = discord.Embed(title="Not connected",colour=0x3DE5C3)
                await ctx.send(embed=embede)
        else:
                self.isvoiceconnected = False
                for x in client.voice_clients:
                    return await x.disconnect()

    #clears the queue but doesnt dc
    async def clear(self,ctx):
            self.playqueue = []
            embede = discord.Embed(title="Queue cleared",colour=0x3DE5C3)
            await ctx.send(embed=embede)


    #starts the player for a given url
    async def startplayer(self,url):
            if not self.isvoiceconnected:
                    print("Not connected to voice")
                    return
            else:
                  try:
                          self.player = await self.voice.create_ytdl_player(url)
                          self.player.start()
                  except:
                          print("Error in creating or starting voice")

    #Unused but will return true once the player finishes the current tjing
    async def checkdone(self,):
            while self.player.is_done() == False:
                    await asyncio.sleep(1)
            return True

    #Like the last one, but for this specific one it will advance the queue and then play the next thing
    async def checkdone_q(self,ctx,channel):
            while self.player.is_done() == False:
                    await asyncio.sleep(1)
            print("Finished")
            await qsubtract(1,False)
            await asyncio.sleep(1)
            try:
                    await play_queue(ctx,channel)
            except:
                    print("Queue ended unknown")

    #is the player is playing, it pauses it
    async def pause(self,ctx):
            if not self.isvoiceconnected:
                    embede = discord.Embed(title="Not connected",colour=0x3DE5C3)
                    await ctx.send(embed=embede)
            else:
                    cond = self.player.is_playing()
                    if cond == True:
                            self.player.pause()
                            embede = discord.Embed(title="Player paused",colour=0x3DE5C3)
                            await ctx.send(embed=embede)
                    else:
                            embede = discord.Embed(title="Not playing",colour=0x3DE5C3)
                            await ctx.send(embed=embede)


    #if the player is paused, it resumes it
    async def resume(self,ctx):
            if not self.isvoiceconnected:
                    embede = discord.Embed(title="Not connected",colour=0x3DE5C3)
                    await ctx.send(embed=embede)
            else:
                    cond = self.player.is_done()
                    if cond == False:
                            self.player.resume()
                            embede = discord.Embed(title="Player resumed",colour=0x3DE5C3)
                            await ctx.send(embed=embede)
                    else:
                            embede = discord.Embed(title="Player done",colour=0x3DE5C3)
                            await ctx.send(embed=embede)

    #Gets some information on the url it is given. It has to load the video first so this is used for thing sthat dont need to be fast, and not in the queue print
    async def getviddeets(self,url="url"):
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
    async def term_to_url(self,searchterm="wheatthings"):
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
    async def q(self,ctx):
            count = 1
            if self.playqueue == []:
                    embede = discord.Embed(title="Error",description="Queue empty",colour=0x3DE5C3)
                    await ctx.send(embed=embede)
            else:
                    q_mess = ""
                    for x in self.playqueue:
                            q_mess = q_mess + (str(count)+"  |  "+ str(self.playqueue[count-1][1])+ "\n")
                            count += 1
                    embede = discord.Embed(title="Queue:",description=q_mess,colour=0x3DE5C3)
                    await ctx.send(embed=embede)

    #adds an item to teh queue, not a command so can be called
    async def qaddition(self,url_in="blankisole"):
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
            if len(self.playqueue) < 10:
                    self.playqueue.append([url,vid_title])
                    success_mess = "Sucessfully added: <" +vid_title+">"
                    embede = discord.Embed(description=success_mess,colour=0x3DE5C3)
                    await ctx.send(embed=embede)
            else:
                    embede = discord.Embed(title="Queue full",colour=0x3DE5C3)
                    await ctx.send(embed=embede)

    #adds 2 q
    async def qadd(self,ctx):
            data = ctx.message.content
            data = data[6:]
            if len(data) == 0:
                    embede = discord.Embed(title="Error",description="Please enter a URL or search term",colour=0x3DE5C3)
                    await ctx.send(embed=embede)
            else:
                    await qaddition(data)



    #same situation as addition, this one needs to be called elsewhere to cannot be a client command
    async def qsubtract(self,place=-1,doprint=False):
            try:
                    place = int(place)
            except:
                    embede = discord.Embed(title="Error",description="Invalid place",colour=0x3DE5C3)
                    await ctx.send(embed=embede)
                    return
            if place < 1 or place > len(self.playqueue):
                    embede = discord.Embed(title="Error",description="Invalid place",colour=0x3DE5C3)
                    await ctx.send(embed=embede)
            else:
                    if doprint == True:
                            success_mess = ("Successfully removed: <" +self.playqueue[place-1][1]+">")
                            embede = discord.Embed(description=success_mess,colour=0x3DE5C3)
                            await ctx.send(embed=embede)
                    self.playqueue.remove(self.playqueue[place-1])

    #yeet
    async def qsub(self,ctx,place=None):
            await qsubtract(place,True)


    #This starts playing the queue in the given voice channel
    async def playq(self,ctx,channel="ohgodmykeeb"):
            if channel not in ["Chub","Barracuda","Pike"]:
                    #await ctx.send("Invalid channel")
                    embede = discord.Embed(title="Error",description="Invalid channel",colour=0x3DE5C3)
                    await ctx.send(embed=embede)
                    return
            if self.isvoiceconnected:
                    isdone = False
                    try:
                            isdone = self.player.is_done()
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
    async def qplay(self,ctx):
            await ctx.send("did you mean playq?")

    #THis is the callable function that starts playing the queue, it calls the other functions to start up the player and connect if it has not already.
    async def play_queue(self,ctx,channel="Nyetcomrade"):
            if channel == "Nyetcomrade":
                    print("Error with connecting to channel")
            if not self.isvoiceconnected:
                    await connectto(ctx,channel)
            if len(self.playqueue) < 1:
                    #await ctx.send("Queue empty")
                    embede = discord.Embed(title="Queue empty",colour=0x3DE5C3)
                    await ctx.send(embed=embede)
            else:
                    await startplayer(self.playqueue[0][0])
                    asyncio.ensure_future(checkdone_q(ctx,channel))
                    return


    #skips currently playing by termninatiing the ytdl stream. Luckily this works really well with the checkdone q function, as that will automatically start playing the next thhing in the right channel
    async def skip(self,ctx):
            if not self.isvoiceconnected:
                    embede = discord.Embed(title="Not connected to voice",colour=0x3DE5C3)
                    await ctx.send(embed=embede)
                    return
            isdone = False
            try:
                    isdone = self.player.is_done()
            except:
                    ""
            if isdone == True:
                    embede = discord.Embed(title="Player done",colour=0x3DE5C3)
                    await ctx.send(embed=embede)
                    return
            else:
                    embede = discord.Embed(title="Skipped",description=self.playqueue[0][1],colour=0x3DE5C3)
                    await ctx.send(embed=embede)
                    self.player.resume() #If the player is paused then stopped it will "stop" the player and it cant be resumed but it leaves a window open and uses memory. If it is resumed first it is a cleaner cut and ffmpeg closes correctly
                    self.player.stop()
