import asyncio
import discord
from discord.ext.commands import Bot
from discord.ext import commands
import lyricsgenius as genius

class geniuscommands():

    def __init__(self):
        pass

    async def lyrics(self,ctx,trackname="Despacito"):
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
