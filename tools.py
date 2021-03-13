from bs4 import BeautifulSoup
from discord.ext import commands
import asyncio
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
}


class MyCog(commands.Cog):
    def __init__(self):
        self.link = ''

    async def news(self, ctx):
        while True:
            news_inside = requests.get('https://thehackernews.com/')
            page = news_inside.content

            info = BeautifulSoup(page, 'lxml')
            final_info = info.find_all('div', class_='body-post clear')

            if self.link != final_info[0].a['href']:
                self.link = final_info[0].a['href']
                await ctx.send(self.link)
            else:
                await asyncio.sleep(5)

    async def collect_ctf(self, ctx):
        news = requests.get('https://ctftime.org/event/list/upcoming', headers=headers)
        page = news.content

        info = BeautifulSoup(page, features='lxml')
        final_info = info.find_all('a', href=True)

        new_list = final_info
        i = 0
        s = 0

        await ctx.send("Top Five Upcoming CTF's")

        while i < 5:
            new_list[s] = str(s) + " " + str(new_list[s])

            if str(new_list[53+i]).find("/event/") != -1:
                digits = await self.number_of_digits(new_list[53+i])

                new = str(new_list[53+i]).replace("<a href=\"", '')
                new = new[:6+digits]

                await ctx.send("https://ctftime.org" + str(new))
                i += 1

            s += 1

    async def number_of_digits(self, part_two):
        part_two = str(part_two).replace("<a href=\"/event/", '')
        part_two = part_two[:3]

        if part_two.isdigit():
            return 5
        else:
            return 4