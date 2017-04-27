import discord, os, asyncio, datetime
from discord.ext import commands
from cogs.utilities import checks, tools
try:
    import cPickle as pickle
except ImportError:
    import pickle

class Admin:
    """Administrator commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, hidden=True)
    async def get_discord_version(self, ctx):
        """Output discord.py version"""
        await self.bot.say("discord.py version: **{}**".format(discord.__version__))

    @commands.command(pass_context=True, hidden=True)
    async def return_id_info(self, ctx, target_id : str):
        if checks.check_owner(ctx.message):
            server = self.bot.get_server(id=target_id)
            if server is None:
                for x in self.bot.servers:
                    if x.get_member(target_id) is not None:
                        server = x
                        break
            channel = self.bot.get_channel(id=target_id)
            member = server.get_member(user_id=target_id)
            await self.bot.say("SERVER: **{}**\nCHANNEL: **{}**\nMEMBER: **{}**".format(server, channel, member))
        else:
            await self.bot.say("You do not have permission to use that command.")

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
        if checks.check_owner(ctx.message) or checks.check_admin(ctx.message):
            await self.bot.send_message(discord.Object(id=str(channel_id)), msg)
            await self.bot.delete_message(ctx.message)

    @commands.command(name='type', pass_context=True, hidden=True)
    async def _type(self, ctx, channel_id : str, *, msg : str):
        if checks.check_owner(ctx.message):
            await self.bot.delete_message(ctx.message)
            await self.bot.send_typing(self.bot.get_channel(channel_id))
            await asyncio.sleep(len(msg) / 7)
            await self.bot.send_message(self.bot.get_channel(channel_id), msg)

    @commands.command(pass_context=True)
    async def clean(self, ctx, search=40):
        """Cleans a few of kamikaze's latest messages"""
        if checks.check_moderator(ctx.message):
            predicate = lambda m: m.author == self.bot.user or m.content.startswith('!k.')
            deleted = await self.bot.purge_from(ctx.message.channel, limit=search+1, check=predicate)
            await asyncio.sleep(1)
            await self.bot.say("Deleted {} message(s).".format(len(deleted)-1), delete_after=6)

    @commands.command(pass_context=True)
    async def list(self, ctx):
        """View a list of Kamikaze's available cogs"""
        if checks.check_admin(ctx.message):
            unInstalledCogs = str([x for x in os.listdir(".\cogs") if x.endswith(".py") and x[:-3] not in (cog.lower() for cog in self.bot.cogs)]).strip('[]').replace("'","").replace(".py", "")
            installedCogs = str([x for x in self.bot.cogs]).strip('[]').replace("'","")
            title = "Kamikaze's Cog Information"
            description ="**Installed cogs:\n**" + installedCogs + "\n\n**Uninstalled cogs:**\n" + unInstalledCogs
            em = tools.createEmbed(title, description)
            await self.bot.say(embed=em)
            #await self.bot.say("Here's my currently installed modules ( ;・w・)7\n```{}```".format(cogsList)) #dont forget to replace them later

    @commands.command(pass_context=True, hidden=True)
    async def _serverSetup(self, ctx):
        """Setup server specific persistence modules"""
        if checks.check_owner(ctx.message) or checks.check_admin(ctx.message):
            serverID = ctx.message.server.id
            await self.bot.delete_message(ctx.message)
            await self.bot.say("Setting up...", delete_after=12)
            try:
                #kamikaze chime
                kamikaze_chime = tools.loadPickle('kamikaze_chime.pickle')
                kamikaze_chime[serverID] = True
                tools.dumpPickle(kamikaze_chime, 'kamikaze_chime.pickle')
                await self.bot.say("**kamikaze_chime** setup success", delete_after=10)
                # END
                await self.bot.say("Setup successful", delete_after=10)
            except Exception as e:
                await self.bot.say("SETUP FAILED\n{}: {}".format(type(e).__name__, e))

    ## UTILITY COMMANDS
    @commands.command(pass_context=True, hidden=True)
    async def cls(self, ctx):
        if checks.check_owner(ctx.message):
            print('\n'*10)

def setup(bot):
    bot.add_cog(Admin(bot))