import discord, asyncio, random
from discord.ext import commands
from cogs.utilities import checks, tools
try:
    import cPickle as pickle
except ImportError:
    import pickle

async def sendChallenge(bot, message, opponent : str):
    opp = message.server.get_member_named(opponent)
    if opp is None:
        await bot.send_message(message.channel, "User not found (case sensitive).")
        return
    elif message.author.name.lower() == opponent.lower():
        await bot.send_message(message.channel, "You cannot challenge yourself...")
        return
    challenge_statement = await bot.send_message(message.channel, "{} has challenged {} to a soku match. Accept? (y/n)".format(message.author.name, opp.mention))
    msg = await bot.wait_for_message(timeout=60, author=opp, check=lambda x: x.content.lower() == 'y' or x.content.lower() == 'n')
    if msg is None:
        await bot.delete_message(challenge_statement)
        return
    else:
        return msg.content.lower() == 'y'

async def wrongServerError(bot, message):
    await bot.send_message(message.channel, "Command must be used in <#{}> in server <{}>".format(bot.get_channel('271935186151669774'), bot.get_server('260977178131431425')))

class Soku:
    """TH 12.3 Hisoutensoku related commands."""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True)
    async def ranked(self, ctx):
        """Kamikaze's Soku ranking system [WIP]"""
        if ctx.invoked_subcommand is None:
            # list options
            pass

    @ranked.command(pass_context=True)
    async def challenge(self, ctx, *, opponent : str):
        """Challenge another opponent to a match of Soku!"""
        MATCH_TIMEOUT = 30
        AUTO_TIMEOUT = 10800 # 3 hours
        if checks.check_soku(ctx.message):
            if await sendChallenge(self.bot, ctx.message, opponent):
                message = ctx.message
                challenger = ctx.message.author
                opp = message.server.get_member_named(opponent)
                #create embed
                title = "Soku: {} vs {}".format(challenger.name, opp.name)
                description = random.choice(["A fight to the death...", "No holds barred..."])
                challenger_wins, opp_wins = 0, 0
                em = tools.createEmbed(title=title, description=description)
                em.add_field(name=challenger.name, value="Matches won: **{}**".format(challenger_wins))
                em.add_field(name=opp.name, value="Matches won: **{}**".format(opp_wins))
                embed_output = await self.bot.say(embed=em)
                prompt = await self.bot.say("Match result for challenger (**w**in/**l**oss/**c**ancel):")
                await asyncio.sleep(MATCH_TIMEOUT)
                msg = await self.bot.wait_for_message(timeout=AUTO_TIMEOUT, author=challenger, check=lambda x: x.content.lower() in 'wlc' and len(x.content) == 1)
                try:
                    while msg.content.lower() != 'c':
                        if msg.content.lower() == 'w':
                            challenger_wins += 1
                            em.set_field_at(index=0, name=challenger.name, value="Matches won: **{}**".format(challenger_wins))
                        elif msg.content.lower() == 'l':
                            opp_wins += 1
                            em.set_field_at(index=1, name=opp.name, value="Matches won: **{}**".format(opp_wins))
                        await self.bot.delete_messages([prompt, msg, embed_output])
                        embed_output = await self.bot.say(embed=em)
                        prompt = await self.bot.say("Match result for challenger: (**w**in/**l**oss/**c**ancel):")
                        await asyncio.sleep(MATCH_TIMEOUT)
                        msg = await self.bot.wait_for_message(timeout=AUTO_TIMEOUT, author=challenger, check=lambda x: x.content.lower() in 'wlc' and len(x.content) == 1)
                    await self.bot.say("Session over")
                except AttributeError:
                    await self.bot.say("{} your soku match with **{}** has timed out...".format(challenger.mention, opp.name))
                    tools.gainCoins(challenger, challenger_wins)
                    tools.gainCoins(opp, opp_wins)
                    return
                # Add coins
                tools.gainCoins(challenger, challenger_wins)
                tools.gainCoins(opp, opp_wins)
            else:
                await self.bot.say("Declined")
        else:
            await wrongServerError(self.bot, ctx.message)

    @commands.group(pass_context=True)
    async def ip(self, ctx):
        """View the Soku IP list."""
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
        """Add yourself to the soku IP list."""
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
        """Add someone else's IP to the list."""
        if checks.check_admin(ctx.message):
            try:
                await self.bot.delete_message(ctx.message)
                soku_ip = tools.loadPickle('soku_ip.pickle')
                if ':' not in ip:
                    ip += ':10800'
                soku_ip[target[0].upper() + target[1:].lower()] = ip
                tools.dumpPickle(soku_ip, 'soku_ip.pickle')
                await self.bot.say("Successfully added {}'s IP to the list.".format(target))
            except Exception as e:
                await self.bot.say("Unable to add {} to the IP list.".format(target))
                #await self.bot.say("{}: {}".format(type(e).__name__, e))

    @ip.command(pass_context=True)
    async def get(self, ctx, *, target : str):
        """Retrieve the target user's IP."""
        soku_ip = tools.loadPickle('soku_ip.pickle')
        # you can only retrieve ips in the soku channel
        if checks.check_soku(ctx.message):
            try:
                soku_ip = tools.loadPickle('soku_ip.pickle')
                try:
                    ip = soku_ip[target[0].upper() + target[1:].lower()]
                    em = tools.createEmbed(title="{}'s Soku IP".format(target[0].upper() + target[1:]), description=ip)
                    await self.bot.say(embed=em, delete_after=60)
                    await self.bot.delete_message(ctx.message)
                except KeyError:
                    await self.bot.say("Unable to find {} in the list.".format(target))
            except Exception as e:
                await self.bot.say("{}: {}".format(type(e).__name__, e))
        else:
            await wrongServerError(self.bot, ctx.message)

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


    @ip.command(pass_context=True, hidden=True)
    async def remove_other(self, ctx, *, target : str):
        """Remove an entry from the soku IP list."""
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
