from discord.ext import commands
from dotenv import load_dotenv
from tools import MyCog
import os

load_dotenv('info.env')
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='-')

bot.add_cog(MyCog())


@bot.command("start_news")
@commands.has_role("President")
async def start_news(ctx):
    get = bot.get_cog("MyCog")
    bot.loop.create_task(get.news(ctx))


@bot.command("ctfs")
@commands.has_role('President')
async def ctf(ctx):
   ctfs = bot.get_cog("MyCog")
   bot.loop.create_task(ctfs.collect_ctf(ctx))


bot.run(TOKEN)