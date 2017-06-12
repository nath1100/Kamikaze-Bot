import discord
from discord.ext import commands
from cogs.utilities import staticData

class Wows:
    """World of Warships related commands."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def sigma(self, *, battleship : str):
        """Retrieve sigma value of a BB"""
        try:
            await self.bot.say("{:.1}{} sigma: **{}**".format(battleship.upper(), battleship.lower()[1:], staticData.sigmaValues(battleship.lower())))
        except Exception as e:
            await self.bot.say('Unable to retrieve sigma for {}'.format(battleship))
            #await self.bot.say('{}: {}'.format(type(e).__name__, e))

def setup(bot):
    bot.add_cog(Wows(bot))