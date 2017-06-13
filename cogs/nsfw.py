import discord
from discord.ext import commands
from cogs.utilities import checks, tools

class Nsfw:
    """Ecchi commands. (///v///)"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def nhentai(self, ctx, *, keywords : str):
        """Search nhentai. Does not support search tags yet. `!k.nhentai random` for random."""
        if checks.check_nsfw(ctx.message):
            if keywords.lower() == "random":
                await self.bot.say("https://nhentai.net/random/")
            else:
                searchUrl = "https://nhentai.net/search/?q="
                """
                "code to parse nhentai-specific keywords should go here
                """
                searchResult = searchUrl + keywords # temporary for lack of tag parsing
                await self.bot.say(searchResult)
        else:
            await self.bot.say("NSFW commands can only be used in NSFW channels!")

def setup(bot):
    bot.add_cog(Nsfw(bot))
