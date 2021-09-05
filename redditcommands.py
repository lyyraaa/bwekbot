import asyncio
import discord
from discord.ext.commands import Bot
from discord.ext import commands
import requests
import requests.auth

class redditcommands():

    def __init__(self,rk1,rk2,rp):
        self.redditkey1 = rk1
        self.redditkey2 = rk2
        self.redditpass = rp

    async def bottomcomment(self,ctx,user):
            client_auth = requests.auth.HTTPBasicAuth(self.redditkey1,self.redditkey2)
            post_data = {"grant_type": "password", "username": "KnackBot", "password": self.redditpass}
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




    async def topcomment(self,ctx,user):
            client_auth = requests.auth.HTTPBasicAuth(self.redditkey1,self.redditkey2)
            post_data = {"grant_type": "password", "username": "KnackBot", "password": self.redditpass}
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
    # Does not work
    async def toppost(self,ctx,subreddit,period="all"):
            if period not in ("day","week","month","year","all"):
                    await ctx.send("Parameters for top: day, week, month, year, all")
                    return
            try:
                    client_auth = requests.auth.HTTPBasicAuth(self.redditkey1,self.redditkey2)
                    post_data = {"grant_type": "password", "username": "KnackBot", "password": self.redditpass}
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
    async def randomsub(self,ctx):
            try:
                    client_auth = requests.auth.HTTPBasicAuth(self.redditkey1,self.redditkey2)
                    post_data = {"grant_type": "password", "username": "KnackBot", "password": self.redditpass}
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
