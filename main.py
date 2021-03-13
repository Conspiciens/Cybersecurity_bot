import requests
from bs4 import BeautifulSoup
import os
import time
from requests_html import HTMLSession
import urllib.request
import re

import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import asyncio

load_dotenv('info.env')
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='-')

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
}


class MyCog(commands.Cog):
    def __init__(self, bot, link):
        self.bot = bot
        self.link = link

    async def news(self, ctx):
        while True:
            news_inside = requests.get('https://thehackernews.com/')
            page = news_inside.content

            info = BeautifulSoup(page, 'lxml')
            final_info = info.find_all('div', class_='body-post clear')

            if (self.link != final_info[0].a['href']):
                self.link = final_info[0].a['href']
                await ctx.send(self.link)
            else:
                await asyncio.sleep(5)


@commands.has_role('President')
@bot.command("start_news")
async def start_news(ctx):
    get = bot.get_cog("MyCog")
    bot.loop.create_task(get.news(ctx))


@bot.command('ctfs')
@commands.has_role('President')
async def ctf(ctx):
    session = HTMLSession()
    r = session.get('https://ctftime.org/event/list/?year=2020&online=-1&format=0&restrictions=-1&upcoming=true')

    print(type(r.html.links))
    new_list = list(r.html.links)
    i = 0
    s = 0

    await ctx.send("Top Five Upcoming CTF's")

    while (i < 6):
        # print(str(new_list[s]))

        if (re.match('^[/event/0-9]*$', str(new_list[s]))):
            print(str(new_list[s]))
            await ctx.send("https://ctftime.org" + str(new_list[s]))
            i += 1

        s += 1


bot.run(TOKEN)