import discord, asyncio, random, datetime, os
from discord.ext import commands
from cogs.utilities import tools, checks, paths
try:
    import cPickle as pickle
except ImportError:
    import pickle

UPLOAD_FOLDER = paths.uploadFolder()

def getCoin(message):
    try:
        if checks.check_hourai(message):
            return "<:coin:303374759687749632>"
        else:
            return ":dollar:"
    except AttributeError:
        return ":dollar:"

class Extras:
    """Miscellaneous commands purely for fun."""

    def __init__(self, bot):
        self.bot = bot

    '''
    @commands.command(pass_context=True)
    async def colour(self, ctx, *, new_colour : str):
        """Change your member colour. !k.colour reset to remove colour."""
        colours = [
            "teal", "dark teal", "green", "dark green", "blue", "dark blue", "purple", "dark purple", "magenta", "dark magenta", "gold",
            "dark gold", "orange", "dark orange", "red", "dark red", "lighter grey", "dark grey", "light grey", "darker grey"
        ]
        if new_colour.lower() == "list":
            title = "List of colours"
            description = ', '.join(colours)
            await self.bot.say(embed=tools.createEmbed(title=title, description=description))
        else:
            #do something
            pass
    '''

    @commands.command(pass_context=True)
    async def up(self, ctx, *, image_name : str):
        """Upload an image from Kamikaze's directory. `!k.up list` for a list of available images."""
        upload_images = [x[:-4] for x in os.listdir(UPLOAD_FOLDER)]
        if image_name == "list":
            await self.bot.say("```{}```".format(', '.join(upload_images)))
        elif image_name in upload_images:
            await self.bot.send_typing(ctx.message.channel)
            try:
                await self.bot.upload(UPLOAD_FOLDER + "\\{}.png".format(image_name))
            except FileNotFoundError:
                await self.bot.upload(UPLOAD_FOLDER + "\\{}.jpg".format(image_name))
        else:
            await self.bot.say("No such image. Try `!k.up list` for a list.")
    
    ''' SHELVED UNTIL SECURE METHOD
    @commands.command(pass_context=True)
    async def down(self, ctx, image_name : str):
        """[missing]"""
        image_data = ctx.message.attachments[0] # only take the first attachment (if there happens to be more than 1)
        if bool([x for x in [".jpg", ".png"] if x in image_data["filename"]]): # return True if filename contains .png or .jpg
            pass
        else:
            await self.bot.say("Please upload a .JPG or .PNG")
    '''

    @commands.group(pass_context=True)
    async def roll(self, ctx):
        """Perform an RNG roll."""
        if ctx.invoked_subcommand is None:
            roll_commands = ["dice", "number"]
            title = "List of roll commands"
            description = '\n'.join(roll_commands)
            em = tools.createEmbed(title=title, description=description)
            await self.bot.say(embed=em)

    @roll.command()
    async def dice(self):
        """Roll a dice."""
        faces = [":one:", ":two:", ":three:", ":four:", ":five:", ":six:"]
        await self.bot.say("You rolled a {}".format(random.choice(faces)))

    @roll.command()
    async def number(self, minimum, maximum):
        """Roll a number between an inclusive range."""
        numbers = {"-":":heavy_minus_sign:","0":":zero:","1":":one:","2":":two:","3":":three:","4":":four:","5":":five:","6":":six:","7":":seven:","8":":eight:","9":":nine:"}
        try:
            value = str(random.randint(int(minimum), int(maximum)))
        except ValueError:
            await self.bot.say("Invalid number range. Do `!k.roll number <min_num> <max_num>`")
            return
        output = ''.join([numbers[x] for x in value])
        await self.bot.say(embed=tools.createEmbed(title="You rolled **{}**".format(output)))

    @commands.command()
    async def poi(self):
        """Poi!"""
        await self.bot.say(embed=tools.createEmbed(title="Poi!"))

    @commands.group(pass_context=True)
    async def coins(self, ctx):
        """View the amount of coins you possess."""
        if ctx.invoked_subcommand is None:
            coinEmoji = getCoin(ctx.message)
            author = ctx.message.author
            try:
                coin_stash = tools.loadPickle("coin_stash.pickle")
                # check if can use custom coin emoji
                title = "{}'s coin purse".format(author.name)
                description ="**{}**x {}".format(coin_stash[author.id], coinEmoji)
                em = tools.createEmbed(title=title, description=description)
                await self.bot.say(embed=em)
                #await self.bot.say("{} has **{}** {}".format(author.mention, coin_stash[author.id], coinEmoji))
            except KeyError:
                await self.bot.say("You do not have any {}...".format(coinEmoji))
                coin_stash[author.id] = 0
                tools.dumpPickle(coin_stash, 'coin_stash.pickle')

    @coins.command(pass_context=True)
    async def all(self, ctx):
        """See how many coins everyone else has."""
        coinEmoji = getCoin(ctx.message)
        coin_stash = tools.loadPickle('coin_stash.pickle')
        description = '\n'.join([("{}: **{}**x {}".format(tools.findMember(self.bot, x).name, coin_stash[x], coinEmoji)) for x in coin_stash])
        title = "Everyone's coin purses"
        em = tools.createEmbed(title=title, description=description)
        await self.bot.say(embed=em)

    @coins.command(pass_context=True)
    async def shop(self, ctx):
        """Seize the means of production!"""
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
        coinEmoji = getCoin(message)
        if message.author == self.bot.user or message.author.bot:
            return
        else:
            # Probablity of gaining a coin from a sent message
            if random.choice([False for x in range(69)] + [True]) and message.channel != self.bot.user and not message.content.startswith('!k.'):
                coin_stash = tools.loadPickle('coin_stash.pickle')
                try:
                    coin_stash[message.author.id] += 1
                except KeyError:
                    coin_stash[message.author.id] = 1
                tools.dumpPickle(coin_stash, 'coin_stash.pickle')
                alert = await self.bot.send_message(message.channel, "{} found a {}".format(message.author.mention, coinEmoji))
                await asyncio.sleep(4)
                await self.bot.delete_message(alert)


def setup(bot):
    bot.add_cog(Extras(bot))
