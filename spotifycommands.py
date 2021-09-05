import asyncio
import discord
from discord.ext.commands import Bot
from discord.ext import commands
import math
import spotipy
import spotipy.util as util

class spotifycommands():

    def __init__(self,token):
        self.token = token
        self.sp = spotipy.Spotify(auth=token)

    async def playlists(self,ctx,username):
        if self.token:
            sp = spotipy.Spotify(auth=self.token)
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

    async def get_artist(self,ctx,name):
        results = self.sp.search(q='artist:' + name, type='artist')
        items = results['artists']['items']
        if len(items) > 0:
            return items[0]
        else:
            return None

    async def show_artist_albums(self,ctx,artist):
        albums = []
        output = []
        results = self.sp.artist_albums(artist['id'], album_type='album')
        albums.extend(results['items'])
        while results['next']:
            results = self.sp.next(results)
            albums.extend(results['items'])
        seen = set() # to avoid dups
        for album in albums:
            name = album['name']
            if name not in seen:
                output.append(name)
                seen.add(name)
        return output

    async def get_album(self,ctx,album):
        results = self.sp.search(q='album:' + album, type='album')
        items = results['albums']['items']
        albumid = items[0]["id"]
        albumurl = items[0]["external_urls"]["spotify"]
        albumcoverurl = items[0]["images"][0]["url"]
        if len(items) > 0:
            return(albumid,albumurl,albumcoverurl)
        else:
            return None

    async def get_track(self,ctx,track):
        results = self.sp.search(q='track:' + track, type='track')
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

    async def gettoptracks(self,ctx,artistid):
        tracks = []
        results = self.sp.artist_top_tracks(ctx,artistid)
        for x in range(5):
            trackalbumname = (results["tracks"][x]["album"]["name"])
            trackname = (results["tracks"][x]["name"])
            output = trackname + "  -  " + trackalbumname
            tracks.append(output)
        return(tracks)

    async def artistalbums(self,ctx,artist):
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

    async def artistinfo(self,ctx,artist):
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

    async def tracklist(self,ctx,album):
        album = await get_album(album)
        if album:
            await ctx.send(album[1])

    async def trackinfo(self,ctx,track):
        track = await get_track(track)
        if track:
            await ctx.send(track[1])
            #print(track[4])
            descrip = "Explicit: "+str(track[3])+"  |  Popularity: "+str(track[0])+"  |  Duration: "+str(track[2])
            embede = discord.Embed(description=descrip,colour=0x1F7A1F)
            await ctx.send(embed=embede)

    async def toptracks(self,ctx,artist):
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
