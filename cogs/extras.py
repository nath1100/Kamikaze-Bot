import discord, asyncio, random, datetime, os, shelve
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

    @commands.group(pass_context=True)
    async def minigame(self, ctx):
        """Various for-fun minigames."""
        if ctx.invoked_subcommand is None:
            await self.bot.say("!k.help minigame for a list of minigames.")

    @minigame.command(pass_context=True)
    async def kanmusu(self, ctx):
        """A game where you attempt to name as many kanmusu as you can.
        Kamikaze will show you a kanmusu, simply type their name. Try to name as many as you can!"""
        player = ctx.message.author
        msg = await self.bot.say("Generating list...")
        with shelve.open("db\\ship_db", "r") as shelf:
            kanmusu_list = list(shelf.keys())
        # Get rid of those fog ships D:
        for fog in ["iona", "haruna (fog)", "takao (fog)"]:
            kanmusu_list.pop(kanmusu_list.index(fog))
        await self.bot.delete_message(msg)
        # GAME LOOP
        alive = True
        AUTO_TIMEOUT = 20 # seconds to name each kanmusu
        correct = 0
        await self.bot.say("You have **{} seconds** to name each kanmusu. You do not need to name Kai suffixes (eg. do Yuudachi, not Yuudcahi Kai Ni). Type **start** to begin.".format(AUTO_TIMEOUT))
        msg = await self.bot.wait_for_message(timeout=120, author=player, check=lambda x: x.content.lower() == "start")
        if msg is None:
            await self.bot.say("Minigame cancelled due to timeout.")
            return
        elif msg.content.lower() == "start":
            while alive and len(kanmusu_list) > 1:
                # randomly select from remaining kanmusu
                full_name = kanmusu_list.pop(kanmusu_list.index(random.choice(kanmusu_list)))
                answer = full_name.split(' ')[0] # randomly select the key, then split it so you chop off the "kai" suffixes
                with shelve.open("db\\ship_db", "r") as shelf:
                    answer_id = shelf[full_name]['id']
                # create the embed
                em = tools.createEmbed(title="Who is this?", description="Player: {}".format(player.name))
                em.set_image(url="https://github.com/Diablohu/WhoCallsTheFleet/blob/master/pics-ships/{}/8.webp?raw=true".format(answer_id))
                em.set_thumbnail(url="https://github.com/Diablohu/WhoCallsTheFleet/blob/master/pics-ships/{}/0.webp?raw=true".format(answer_id))
                #em.set_footer(text=answer_id) # FOR DEBUGGING ID
                question = await self.bot.say(embed=em)
                # wait for a response from the player
                response = await self.bot.wait_for_message(timeout=AUTO_TIMEOUT, author=player, check=lambda x: x.content.lower() == answer.lower())
                if response is None:
                    # timeout  - wrong answer / no response
                    await self.bot.say("Out of Time! The answer is **{}**".format(answer))
                    alive = False
                    await asyncio.sleep(5)
                    await self.bot.delete_message(question)
                elif response.content.lower() == answer.lower():
                    # answer is correct
                    fanfare = await self.bot.say("Correct!")
                    await asyncio.sleep(2)
                    await self.bot.delete_messages([fanfare, response, question])
                    correct += 1
            await self.bot.say("You correctly named **{}** kanmusu!".format(correct))

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
        #description = '\n'.join([("{}: **{}**x {}".format(tools.findMember(self.bot, x).name, coin_stash[x], coinEmoji)) for x in coin_stash])
        #title = "Everyone's coin purses"
        description = "The 5 richest users."
        title = "Coin Ranking"
        em = tools.createEmbed(title=title, description=description)
        for position in range(1, 6):
            rich_user = max(coin_stash, key=coin_stash.get)
            em.add_field(name="{}. {}".format(position, tools.findMember(self.bot, rich_user).name), value="{}x {}".format(coin_stash[rich_user], coinEmoji))
            coin_stash.pop(rich_user)
        await self.bot.say(embed=em)

    @commands.command(pass_context=True)
    async def zine(self, ctx):
        """Submit an image for the Houraigekisen, Yoi! magazine :)
        Upload an image along with the command in order to submit the image.
        Only for Houraigekisen, Yoi! members."""
        if checks.check_hourai(ctx.message):
            ZINE_CHANNEL = "435411661457981440"
            try:
                url = ctx.message.attachments[0]['url']
                if any([x in url.lower() for x in [".png", ".jpg"]]):
                    await self.bot.send_message(self.bot.get_channel(id=ZINE_CHANNEL), url)
                    await self.bot.say("Added image to the zine :>")
                else:
                    await self.bot.say("Please upload a PNG or JPG image.")
            except IndexError:
                await self.bot.say("Please upload your image along with `!k.zine`.")
            

    async def on_message(self, message):
        coinEmoji = getCoin(message)
        if message.author == self.bot.user or message.author.bot:
            return
        else:
            # Probablity of gaining a coin from a sent message
            if random.choice([False for x in range(69)] + [True]) and message.channel != self.bot.user and message.content[:3] != "!k.":
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
