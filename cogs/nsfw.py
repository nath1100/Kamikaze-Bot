import discord
from discord.ext import commands

class Nsfw:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def nhentai(self, ctx, *, keywords : str):
        """Search nhentai. Does not support search tags yet. "Random" for random."""
        if keywords.lower() == "random":
            await self.bot.send_message(ctx.message.author, "https://nhentai.net/random/")
        else:    
            searchUrl = "https://nhentai.net/search/?q="
            """
            "code to parse nhentai-specific keywords should go here
            """
            searchResult = searchUrl + keywords # temporary for lack of tag parsing
            await self.bot.send_message(ctx.message.author, searchResult)



def setup(bot):
    bot.add_cog(Nsfw(bot))