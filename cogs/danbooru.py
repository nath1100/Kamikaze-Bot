import discord, requests, json
from bs4 import BeautifulSoup
from discord.ext import commands

class Danbooru:
    """Various commands that utilise the danbooru API"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def danbooru(self, ctx, tag_name : str, image_limit : int):
        """Kamikaze will PM you the first 10 danbooru images related to the tag"""
        page = requests.get("https://danbooru.donmai.us/posts.json?limit={}&tags={}".format(image_limit, tag_name))
        data = json.loads(str(BeautifulSoup(page.content, 'html.parser')))
        try:
            for x in range(image_limit):
                await self.bot.send_message(ctx.message.author, "https://danbooru.donmai.us"+data[x]["large_file_url"] + "\n")
        except IndexError:
            await self.bot.send_message(ctx.message.channel, 'Sorry, either the tag was non-existent or cooldown (500 per hour) has been activated.')


def setup(bot):
    bot.add_cog(Danbooru(bot))