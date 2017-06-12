import discord
from discord.ext import commands
from cogs.utilities import checks

class Loader:
    """Commands for loading and unloading cogs."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, hidden=True)
    async def load(self, ctx, cog : str):
        """Loads an extension"""
        if checks.check_owner(ctx.message):
            try:
                self.bot.load_extension(cog)
            except Exception as e:
                await self.bot.say('Unable to load ' + cog)
                await self.bot.say('{}: {}'.format(type(e).__name__, e))
            else:
                await self.bot.say('Successfully loaded ' + cog)

    @commands.command(pass_context=True, hidden=True)
    async def unload(self, ctx, cog : str):
        """Unloads an extension"""
        if checks.check_owner(ctx.message):
            try:
                self.bot.unload_extension(cog)
            except Exception as e:
                await self.bot.say('Could not unload ' + cog)
                await self.bot.say('{}: {}'.format(type(e).__name__, e))
            else:
                await self.bot.say('Successfully unloaded ' + cog)

    @commands.command(name='reload', pass_context=True, hidden=True)
    async def _reload(self, ctx, cog : str):
        """Reloads an extension"""
        if checks.check_owner(ctx.message):
            try:
                self.bot.unload_extension(cog)
                self.bot.load_extension(cog)
            except Exception as e:
                await self.bot.say('Unable to reload ' + cog)
                await self.bot.say('{}: {}'.format(type(e).__name__, e))
            else:
                await self.bot.say('Successfully reloaded ' + cog)


def setup(bot):
    bot.add_cog(Loader(bot))