import discord, asyncio, random, datetime
from discord.ext import commands
from cogs.utilities import tools, checks
try:
    import cPickle as pickle
except ImportError:
    import pickle

class Extras:

    def __init__(self, bot):
        self.bot = bot
        self.coin_emoji = "<:coin:303374759687749632>"

    @commands.group(pass_context=True)
    async def coins(self, ctx):
        """How many coins do you have?"""
        if ctx.invoked_subcommand is None:
            author = ctx.message.author
            try:
                coin_stash = tools.loadPickle("coin_stash.pickle")
                title = "{}'s coin purse".format(author.name)
                description ="**{}**x {}".format(coin_stash[author.id], self.coin_emoji)
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
        description = '\n'.join([("{}: **{}**x {}".format(ctx.message.server.get_member(x).name, coin_stash[x], self.coin_emoji)) for x in coin_stash])
        title = "Everyone's coin purses"
        em = tools.createEmbed(title=title, description=description)
        await self.bot.say(embed=em)

    @coins.command(pass_context=True)
    async def shop(self, ctx):
        """Seize the means of production"""
        wordMonths = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        dateSuffix = ['th', 'st', 'nd', 'rd', 'th', 'th', 'th', 'th', 'th', 'th']
        today = datetime.datetime.today()
        title = "Goods for the {}{} of {}".format(today.day, dateSuffix[today.day % 10], wordMonths[today.month - 1])
        # retrieve past shop information from pickle
        # evaluate whether old or current
        # change shop contents if required and save to pickle
        description = "Nothing in stock..." # temp
        em = tools.createEmbed(title=title, description=description)
        await self.bot.say(embed=em)

    async def on_message(self, message):
        if message.author == self.bot.user or message.author.bot:
            return
        else:
            # Probablity of gaining a coin from a sent message
            if random.choice([False for x in range(59)] + [True]) and message.channel != self.bot.user and message.server.id == "260977178131431425" and not message.content.startswith('!k.'):
                coin_stash = tools.loadPickle('coin_stash.pickle')
                try:
                    coin_stash[message.author.id] += 1
                except KeyError:
                    coin_stash[message.author.id] = 1
                tools.dumpPickle(coin_stash, 'coin_stash.pickle')
                alert = await self.bot.send_message(message.channel, "{} found a {}:".format(message.author.mention, self.coin_emoji))
                await asyncio.sleep(4)
                await self.bot.delete_message(alert)


def setup(bot):
    bot.add_cog(Extras(bot))