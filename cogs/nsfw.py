import discord
from discord.ext import commands
from cogs.utilities import checks, tools

class Nsfw:
    """Ecchi commands. (///v///)
    [Removed]"""

    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(Nsfw(bot))
