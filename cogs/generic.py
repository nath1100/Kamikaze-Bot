import datetime, discord, asyncio, random, os
from discord.ext import commands
from cogs.utilities import paths

#constants
upload_folder = paths.uploadFolder()

class Generic:
    """A range of general and misc commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def fact(self):
        """Receive a random fact from Kamikaze"""
        with open('fact_database', 'r') as f:
            chosen_fact = str(random.choice(f.readlines()))
        await self.bot.say('```{}```'.format(chosen_fact))

    @commands.command()
    async def up(self, item : str):
        """Display a file from Kamikaze's directory."""
        if '\\' in item:
            pass
        elif item == 'list':
            item_list = []
            for x in os.listdir(upload_folder):
                item_list.append(str(x).strip('[]'))
            await self.bot.say('```{}```'.format(item_list))
        elif item in os.listdir(upload_folder): # make certain to keep kamikaze_bot.py in her directory, and that the file dir is correct
            await self.bot.upload(upload_folder + '\\' + item)
        else:
            try:
                await self.bot.upload(upload_folder + '\\{}.jpg'.format(item))
            except Exception:
                try:
                    await self.bot.upload(upload_folder + '\\{}.png'.format(item))
                except Exception:
                    pass

    @commands.command(pass_context=True)
    async def ping(self, ctx):
        """Ping Kamikaze"""
        await self.bot.say('Pong~')

    @commands.command(pass_context=True)
    async def info(self, ctx):
        """Retrieve server information"""
        try:
            data = ""
            data += "Server owner: {}#{}\n".format(ctx.message.server.owner.name, ctx.message.server.owner.discriminator)
            data += "Server region: {}\n".format(ctx.message.server.region)
            adminList = []
            for member in ctx.message.server.members:
                if ctx.message.channel.permissions_for(member).administrator:
                    adminList.append(member.name)
            data += "Administrators: {}\n".format(str(adminList).strip('[]').replace("'",""))
            await self.bot.say("```{}```".format(data))
        except Exception as e:
            await self.bot.say("{}: {}".format(type(e).__name__, e))

def setup(bot):
    bot.add_cog(Generic(bot))