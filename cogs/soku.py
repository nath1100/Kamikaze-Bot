import discord
from discord.ext import commands
from cogs.utilities import checks, tools
try:
    import cPickle as pickle
except ImportError:
    import pickle

class Soku:
    """TH12.3 Hisoutensoku related commands"""
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True)
    async def ranking(self, ctx):
        """Kamikaze's Soku ranking system [WIP]"""
        if ctx.invoked_subcommand is None:
            # list options
            pass

    @commands.group(pass_context=True)
    async def ip(self, ctx):
        """Soku IP related commands"""
        if ctx.invoked_subcommand is None:    
            soku_ip = tools.loadPickle('soku_ip.pickle')
            try:
                all_ip = ''
                for x in soku_ip:
                    ip = soku_ip[x]
                    for y in range(10):
                        ip = ip.replace(str(y), 'x')
                    ip = soku_ip[x].split('.')[0] + '.' + '.'.join(ip.split('.')[1:])
                    all_ip += '{}: **{}**\n'.format(x, ip)
                await self.bot.say(embed=tools.createEmbed(title="Houraigekisen Soku IP list", description=all_ip))
            except Exception as e:
                await self.bot.say('{}: {}'.format(type(e).__name__, e))

    @ip.command(pass_context=True)
    async def add(self, ctx, ip : str):
        """Add yourself to the soku IP list"""
        await self.bot.delete_message(ctx.message)
        soku_ip = tools.loadPickle('soku_ip.pickle')
        soku_ip[ctx.message.author.name] = ip
        if ':' not in ip:
            ip += ':10800'
        try:
            tools.dumpPickle(soku_ip, 'soku_ip.pickle')
            await self.bot.say("Successfully added {} to the IP list.".format(ctx.message.author.name))
        except Exception as e:
            await self.bot.say('Unable to add to IP list')
            #await self.bot.say('{}: {}'.format(type(e).__name__, e))

    @ip.command(pass_context=True, hidden=True)
    async def add_other(self, ctx, target : str, ip : str):
        """Add someone else's IP to the list"""
        if checks.check_admin(ctx.message):
            try:
                await self.bot.delete_message(ctx.message)
                soku_ip = tools.loadPickle('soku_ip.pickle')
                soku_ip[target[0].upper() + target[1:].lower()] = ip
                tools.dumpPickle(soku_ip, 'soku_ip.pickle')
                await self.bot.say("Successfully added {}'s IP to the list.".format(target))
            except Exception as e:
                await self.bot.say("Unable to add {} to the IP list.".format(target))
                #await self.bot.say("{}: {}".format(type(e).__name__, e))

    @ip.command(pass_context=True)
    async def get(self, ctx, target : str):
        """Retrieve the target user's IP"""
        soku_ip = tools.loadPickle('soku_ip.pickle')
        # you can only retrieve ips in the soku channel
        if checks.check_soku(ctx.message):
            try:
                soku_ip = tools.loadPickle('soku_ip.pickle')
                try:
                    ip = soku_ip[target[0].upper() + target[1:].lower()]
                    em = tools.createEmbed(title="{}'s Soku IP".format(target[0].upper() + target[1:]), description=ip)
                    await self.bot.say(embed=em, delete_after=30)
                except KeyError:
                    await self.bot.say("Unable to find {} in the list.".format(target))
            except Exception as e:
                await self.bot.say("{}: {}".format(type(e).__name__, e))
        else:
            await self.bot.say("Command must be used in <#{}> in server <{}>".format(self.bot.get_channel('271935186151669774'), self.bot.get_server('260977178131431425')))

    @ip.command(pass_context=True)
    async def remove(self, ctx):
        """Remove your IP from the soku IP list."""
        try:
            soku_ip = tools.loadPickle('soku_ip.pickle')
            soku_ip.pop(ctx.message.author.name)
            tools.dumpPickle(soku_ip, 'soku_ip.pickle')
            await self.bot.say("Successfully removed {} from the list".format(ctx.message.author.name))
        except KeyError:
            await self.bot.say("You are not in the soku IP list.")
        except Exception as e:
            await self.bot.say("{}: {}".format(type(e).__name__, e))


    @commands.command(pass_context=True, hidden=True)
    async def remove_other(self, ctx, target):
        """Remove an entry from the soku IP list"""
        if checks.check_admin(ctx.message):
            try:
                soku_ip = tools.loadPickle('soku_ip.pickle')
            except Exception as e:
                await self.bot.say("{}: {}".format(type(e).__name__, e))
            try:
                soku_ip.pop(target)
                await self.bot.say("{} was removed from the list.".format(target))
                tools.dumpPickle(soku_ip, 'soku_ip.pickle')
            except KeyError:
                try:
                    # retry after applying case sensitive modifications
                    soku_ip.pop(target[0].upper() + target[1:].lower())
                    tools.dumpPickle(soku_ip, 'soku_ip.pickle')
                    await self.bot.say("{} was removed from the list.".format(target))
                except KeyError:
                    await self.bot.say("Unable to find {} in the IP list".format(target))
            except Exception as e:
                pass
                #await self.bot.say("{}: {}".format(type(e).__name__, e))

def setup(bot):
    bot.add_cog(Soku(bot))