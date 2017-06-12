import discord
from discord.ext import commands
from cogs.utilities import checks, tools

class Nsfw:
    """Ecchi commands. (///v///)"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, hidden=True)
    async def nsfw_enable(self, ctx):
        """Enables NSFW commands for the current channel"""
        if checks.check_moderator(ctx.message):
            channel_list = tools.loadPickle('nsfwChannels.pickle')
            if not checks.check_nsfwEnabled(ctx.message):
                channel_list.append(ctx.message.channel.id)
                tools.dumpPickle(channel_list, 'nsfwChannels.pickle')
                await self.bot.say("NSFW commands **enabled** for this channel.")
            else:
                await self.bot.say("NSFW commands are **already enabled** for this channel.")

    @commands.command(pass_context=True, hidden=True)
    async def nsfw_disable(self, ctx):
        """Disables NSFW commands for the current channel"""
        if checks.check_moderator(ctx.message):
            channel_list = tools.loadPickle('nsfwChannels.pickle')
            if checks.check_nsfwEnabled(ctx.message):
                channel_list.pop(channel_list.index(ctx.message.channel.id))
                tools.dumpPickle(channel_list, 'nsfwChannels.pickle')
                await self.bot.say("NSFW commands **disabled** for this channel.")
            else:
                await self.bot.say("NSFW commands **already disabled** for this channel.")

    @commands.command(pass_context=True)
    async def nhentai(self, ctx, *, keywords : str):
        """Search nhentai. Does not support search tags yet. "Random" for random."""
        if checks.check_nsfwEnabled(ctx.message):
            if keywords.lower() == "random":
                await self.bot.send_message(ctx.message.author, "https://nhentai.net/random/")
            else:
                searchUrl = "https://nhentai.net/search/?q="
                """
                "code to parse nhentai-specific keywords should go here
                """
                searchResult = searchUrl + keywords # temporary for lack of tag parsing
                await self.bot.send_message(ctx.message.author, searchResult)
        else: # revise checks.check_nsfwEnabled() so that this else isn't needed for every command.
            await self.bot.send_message(ctx.message.channel, "NSFW commands are disabled for this channel. Sorry! (> ||| <)")

def setup(bot):
    bot.add_cog(Nsfw(bot))