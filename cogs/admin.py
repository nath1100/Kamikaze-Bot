import discord, os, asyncio
from discord.ext import commands
from cogs.utilities import checks
try:
    import cPickle as pickle
except ImportError:
    import pickle

class Admin:
    """Administrator commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, hidden=True)
    async def close(self, ctx):
        if checks.check_owner(ctx.message):
            await self.bot.say('Bye Teitoku~')
            await self.bot.close()

    @commands.command(pass_context=True, hidden=True)
    async def status(self, ctx, *, new_status : str):
        if checks.check_owner(ctx.message):
            kamikaze_status = []
            kamikaze_status.append(new_status)
            await self.bot.change_presence(game=discord.Game(name=kamikaze_status[0]))
            with open('kamikaze_status.pickle', 'wb') as f:
                pickle.dump(kamikaze_status, f)

    @commands.command(name='say', pass_context=True, hidden=True)
    async def _say(self, ctx, channel_id : str, *, msg : str):
        if checks.check_owner(ctx.message):
            await self.bot.send_message(discord.Object(id=str(channel_id)), msg)

    @commands.command(pass_context=True)
    async def clean(self, ctx, search=20):
        """Cleans a few of kamikaze's latest messages"""
        if checks.check_moderator(ctx.message):
            predicate = lambda m: m.author == self.bot.user or m.content.startswith('!k.')
            deleted = await self.bot.purge_from(ctx.message.channel, limit=search+1, check=predicate)
            await asyncio.sleep(1)
            await self.bot.say("Deleted {} message(s).".format(len(deleted)-1))

    @commands.command(pass_context=True)
    async def list(self, ctx):
        """View list of available cogs"""
        if checks.check_admin(ctx.message):
            items = os.listdir(".\cogs")
            cogsList = ''
            for cogs in items:
                if cogs.endswith(".py"):
                    cogsList += (cogs[:-3] + '\n')
            await self.bot.say("Here's my currently installed modules ( ;・w・)7\n```{}```".format(cogsList)) #dont forget to replace them later

    ## UTILITY COMMANDS
    @commands.command(pass_context=True, hidden=True)
    async def cls(self, ctx):
        if checks.check_owner(ctx.message):
            print('\n'*10)

def setup(bot):
    bot.add_cog(Admin(bot))