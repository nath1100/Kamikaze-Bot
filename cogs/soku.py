import discord, asyncio, random
from discord.ext import commands
from cogs.utilities import checks, tools
try:
    import cPickle as pickle
except ImportError:
    import pickle

async def sendChallenge(bot, message, opponent : str):
    opp = message.server.get_member_named(opponent)
    while opp is None:
        await bot.send_message(message.channel, "User not found (case sensitive).")
        return
    await bot.send_message(message.channel, "{} has challenged {} to a soku match. Accept? (y/n)".format(message.author.name, opp.mention))
    msg = await bot.wait_for_message(author=opp, check=lambda x: x.content.lower() == 'y' or x.content.lower() == 'n')
    return msg.content.lower() == 'y'

async def wrongServerError(bot, message):
    await bot.send_message(message.channel, "Command must be used in <#{}> in server <{}>".format(bot.get_channel('271935186151669774'), bot.get_server('260977178131431425')))

class Soku:
    """TH12.3 Hisoutensoku related commands"""
    def __init__(self, bot):
        self.bot = bot
        self.coin_emoji = "<:coin:303374759687749632>"

    @commands.group(pass_context=True)
    async def ranked(self, ctx):
        """Kamikaze's Soku ranking system [WIP]"""
        if ctx.invoked_subcommand is None:
            # list options
            pass

    @ranked.command(pass_context=True)
    async def challenge(self, ctx, *, opponent : str):
        """Challenge another opponent!"""
        MATCH_TIMEOUT = 1
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
                msg = await self.bot.wait_for_message(author=challenger, check=lambda x: x.content.lower() in 'wlc' and len(x.content) == 1)
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
                    msg = await self.bot.wait_for_message(author=challenger, check=lambda x: x.content.lower() in 'wlc' and len(x.content) == 1)
                await self.bot.say("Session over")
            else:
                await self.bot.say("Declined")
        else:
            await wrongServerError(self.bot, ctx.message)

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

    @commands.group(pass_context=True)
    async def coins(self, ctx):
        """How many coins do you have?"""
        if ctx.invoked_subcommand is None:
            author = ctx.message.author
            try:
                coin_stash = tools.loadPickle("coin_stash.pickle")
                title = "{}'s coin purse".format(author.name)
                description ="**{}** {}".format(coin_stash[author.id], self.coin_emoji)
                em = tools.createEmbed(title=title, description=description)
                await self.bot.say(embed=em)
                #await self.bot.say("{} has **{}** {}".format(author.mention, coin_stash[author.id], self.coin_emoji))
            except KeyError:
                await self.bot.say("You do not have any {}...".format(self.coin_emoji))
                coin_stash[author.id] = 0
                tools.dumpPickle(coin_stash, 'coin_stash.pickle')

    @coins.command(pass_context=True)
    async def all(self, ctx):
        """Check other people's coins"""
        coin_stash = tools.loadPickle('coin_stash.pickle')
        description = '\n'.join([("{}: {} {}".format(ctx.message.server.get_member(x).name, coin_stash[x], self.coin_emoji)) for x in coin_stash])
        title = "Everyone's coin purses"
        em = tools.createEmbed(title=title, description=description)
        await self.bot.say(embed=em)

    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        else:
            # Probablity of gaining a coin from a sent message
            if random.choice([False for x in range(69)] + [True]) and message.channel != self.bot.user and message.server.id == "260977178131431425":
                coin_stash = tools.loadPickle('coin_stash.pickle')
                try:
                    coin_stash[message.author.id] += 1
                except KeyError:
                    coin_stash[message.author.id] = 1
                tools.dumpPickle(coin_stash, 'coin_stash.pickle')
                alert = await self.bot.send_message(message.channel, "{} found a {}:".format(message.author.mention, self.coin_emoji))
                await asyncio.sleep(3)
                await self.bot.delete_message(alert)

def setup(bot):
    bot.add_cog(Soku(bot))