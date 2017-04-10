import discord, requests, json, wikipedia
from bs4 import BeautifulSoup
from discord.ext import commands
from cogs.utilities import checks, tools

class Internet:
    """Various commands that pull internet data"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def wikipedia(self, ctx, *, search : str):
        """Search for articles on wikipedia"""
        results = wikipedia.search(search, results=6)
        if results == []:
           await self.bot.say("No results found for **{}**...".format(search))
           return
        description = "**Please select a number:**\n"
        # Create a numbered, '\n' separated str from list <results> and add to the description str
        description += '\n'.join([( "**{}**. {}".format(results.index(x) + 1, x) )  for x in results])
        description += "\n\n**0**. Cancel search"
        em = tools.createEmbed(title="Search results for {}".format(search), description=description)
        await self.bot.say(embed=em)
        msg = await self.bot.wait_for_message(author=ctx.message.author, check=lambda x: checks.convertsToInt(x.content) and int(x.content) in range(len(results) + 1))
        if int(msg.content) == 0:
            await self.bot.say("Search cancelled.")
            return
        article_title = results[int(msg.content) - 1]
        page = wikipedia.page(article_title)
        em = tools.createEmbed(title="Result #{}: {}".format(msg.content, article_title), description=page.summary)
        await self.bot.say(embed=em)

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
    bot.add_cog(Internet(bot))