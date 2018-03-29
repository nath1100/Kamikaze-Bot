import asyncio, discord, random, shelve
from discord.ext import commands
from datetime import datetime
from cogs.utilities import checks, paths, staticData, tools
try:
    import cPickle as pickle
except ImportError:
    import pickle

#constants
upload_folder = paths.uploadFolder()

def createExpeditionEmbed(data):
    title = "Expedition {}: {}".format(data["id"], data["name"])
    description = "Ships: **{}**".format(data["requirements"]["ships"])
    description += "\nDrums: **{}**".format(data["requirements"]["drums"])
    time_h, time_m = divmod(data["time"], 60)
    description += "\nTime: **{}:{:02.0f}**".format(time_h, time_m)
    em = tools.createEmbed(title=title, description=description)

    # level requirements
    value0 = "Flagship: **{}**\nTotal: **{}**".format(data["requirements"]["fs"], data["requirements"]["total"])
    em.add_field(name="Level Requirements", value=value0, inline=False)

    # hourly yields
    value1 = "Resources: {}".format(" / ".join(str(x) for x in data["yield"]["hourly"]))
    value1 += "\nHQ xp: {}\nShip xp: {}".format(data["exp"]["hourly"]["hq"], data["exp"]["hourly"]["ship"])
    em.add_field(name="Hourly Yield", value=value1, inline=False)

    # total yields
    value2 = "Resources: {}".format(" / ".join(str(x) for x in data["yield"]["total"]))
    value2 += "\nHQ xp: {}\nShip xp: {}".format(data["exp"]["total"]["hq"], data["exp"]["total"]["ship"])
    em.add_field(name="Total Yield", value=value2, inline=False)

    # rewards
    value3 = "Common: {}\nGreat Success: {}".format(data["reward"][0], data["reward"][1])
    em.add_field(name="Rewards", value=value3, inline=False)

    # great success rewards
    gs_hourly = " / ".join(str(int(y)) for y in [x*1.5 for x in data["yield"]["hourly"]])
    gs_total = " / ".join(str(int(y)) for y in [x*1.5 for x in data["yield"]["total"]])
    value4 = "Hourly: {}\nTotal: {}".format(gs_hourly, gs_total)
    em.add_field(name="Great Success Yields", value=value4, inline=False)

    return em

async def oaswSuggestions(bot, ctx, kanmusu):
    kanmusu = kanmusu.lower()
    if kanmusu == 'hibiki':
        suggestion = 'Verniy, Bep'
        await bot.send_message(ctx.message.channel, "Perhaps you meant _{}_".format(suggestion))

class Kancolle:
    """Commands related to Kantai Collection."""

    def __init__(self, bot):
        self.bot = bot
        #KC EVENT TIMER
        self.event_countdown = bot.loop.create_task(self.calc_countdown())

    def __unload(self):
        self.event_countdown.cancel()

    async def calc_countdown(self):
        await self.bot.wait_until_ready()
        FREQ = 60 # run task every minute
        message_id = "421155838439194633"
        event_channel = self.bot.get_channel("414474883360358410")
        countdown_message = await self.bot.get_message(channel=event_channel, id=message_id)
        TARGET_TIME = datetime(2018, 3, 23, 13)
        while not self.bot.is_closed:
            time_left = TARGET_TIME - datetime.now()
            d, s = time_left.days, time_left.seconds
            weeks, days = divmod(d, 7)
            m, seconds = divmod(s, 60)
            hours, minutes = divmod(m, 60)
            em = tools.createEmbed(title="Time Remaining", description="{} weeks, {} days, {} hours, {} minutes".format(weeks, days, hours, minutes))
            em.set_footer(text="Updates every {} second(s)".format(FREQ))
            await self.bot.edit_message(message=countdown_message, embed=em)
            await asyncio.sleep(FREQ)

    @commands.command()
    async def expedition(self, exped_number : str):
        """Lookup the data for a certain expedition."""
        with shelve.open("db\\expedition_db\\exped_db", "r") as shelf:
            try:
                data = shelf[exped_number]
            except KeyError:
                await self.bot.say("Could not find expedition `{}`".format(exped_number))
                return
        em = createExpeditionEmbed(data)
        await self.bot.say(embed=em)

    @commands.command()
    async def compareships(self, *, args : str):
        """Compare the stats of two kanmusu with `!k.comapreships <ship1>, <ship2>`
        or lookup stats with `!k.compareships <ship>`"""
        ZERO_STAT_COMPARATOR = "0_stat"
        if ', ' not in args:
            firstShip = args
            secondShip = ZERO_STAT_COMPARATOR
        else:
            try:
                firstShip, secondShip = args.split(', ')
            except ValueError:
                await self.bot.say("`!k.compareships ship1, ship2` for stat comparison. `!k.compareships ship` for stat lookup.")
                return
        with shelve.open("db\\ship_db", "r") as shelf:
            try:
                ship1 = shelf[firstShip.lower()]
            except KeyError:
                await self.bot.say("Unable to find **{}**.".format(firstShip))
                if ', ' not in args:
                    await self.bot.say("Did you forget the comma? `!k.compareships ship1, ship2`")
                return
            try:
                ship2 = shelf[secondShip.lower()]
            except KeyError:
                await self.bot.say("Unable to find **{}**.".format(secondShip))
                if ', ' not in args:
                    await self.bot.say("Did you forget the comma? `!k.compareships ship1, ship2`")
                return
        if ship1 is None or ship2 is None:
            return
        else:
            #build the embed
            firstShipFormatted, secondShipFormatted = firstShip[0].upper() + firstShip[1:].lower(), secondShip[0].upper() + secondShip[1:].lower()
            if secondShip is not ZERO_STAT_COMPARATOR:
                title = "{}'s stats VS {}".format(firstShipFormatted, secondShipFormatted)
                description = "Comparing max stats (except luck)"
            else:
                title = "{}'s stats".format(firstShipFormatted)
                description = "{} stat lookup".format(firstShipFormatted)
            em = tools.createEmbed(title=title, description=description)
            em.set_image(url="https://github.com/Diablohu/WhoCallsTheFleet/blob/master/pics-ships/{}/0.webp?raw=true".format(ship1['id']))
            stats = [
                ('fire_max', 'Firepower'),
                ('torpedo_max', 'Torpedo'),
                ('aa_max', 'AA'),
                ('asw_max', 'ASW'),
                ('hp', 'HP'),
                ('armor_max', 'Armour'),
                ('evasion_max', 'Evasion'),
                ('luck', 'Luck'),
                ('fuel', 'Fuel Consumption'),
                ('ammo', 'Ammo Consumption'),
                ('base_lvl', 'Base Level'),
                ('slot', 'Plane Slots')
            ]
            for stat in stats:
                if ship1[stat[0]] == -1 or ship2[stat[0]] == -1:
                    statResult = 'No Data'
                elif stat[0] == "slot":
                    if secondShip != ZERO_STAT_COMPARATOR:
                        statResult = "{}: **{}**\n{}: **{}**".format(firstShipFormatted, ship1[stat[0]], secondShipFormatted, ship2[stat[0]])
                    else:
                        statResult = ship1[stat[0]]
                else:
                    statResult = ship1[stat[0]] - ship2[stat[0]]
                    if statResult > 0 and secondShip != ZERO_STAT_COMPARATOR:
                        statResult = "**+{}**".format(statResult)
                em.add_field(name=stat[1], value=statResult)
            await self.bot.say(embed=em)

    '''
    @commands.command(pass_context=True)
    async def lbas_range(self, ctx, shortest_range : int):
        """Display LBAS range bonuses given the lowest equipped aircraft range."""
        try:
            data = staticData.lbasRangeData(shortest_range)
            output = 'LBAS range bonuses:\n'
            for x in data:
                output += "{}:\n{:>4}\n\n".format(x, data[x])
            await self.bot.say("```{}```".format(output))
        except IndexError:
            await self.bot.say("Please enter a range between 2 and 9.")

    @commands.command(pass_context=True)
    async def lbasrange(self, ctx, lowest_range=None):
        """Display the LBAS range bonuses given by various recon aircraft."""
        if lowest_range is None:
            try:
                await self.bot.send_typing(ctx.message.channel)
                await self.bot.upload(upload_folder + "\\" + "lbas_range.png")
            except FileNotFoundError:
                await self.bot.upload(upload_folder + "\\" + "lbas_range.jpg")
        else:
            try:
                data = staticData.lbasRangeData(lowest_range)
                output = "LBAS range bonusses:\n" + "\n".join(["{}:\n{:>4}\n".format(x, data[x]) for x in data])
                await self.bot.say("```{}```".format(output))
            except IndexError:
                await self.bot.say("Please enter a range between 2 and 9")
    '''

    @commands.group(pass_context=True)
    async def lbas(self, ctx):
        """Display LBAS aircraft information."""
        if ctx.invoked_subcommand is None:
            await tools.uploadImage(self.bot, ctx, filename="lbas")

    @lbas.command(pass_context=True)
    async def range(self, ctx, lowest_range=None):
        """Display the LBAS range bonuses given by various recon aircraft."""
        if lowest_range is None:
            await tools.uploadImage(self.bot, ctx, filename="lbas_range")
        else:
            try:
                data = staticData.lbasRangeData(lowest_range)
                output = "LBAS range bonusses:\n" + "\n".join(["{}:\n{:>4}\n".format(x, data[x]) for x in data])
                await self.bot.say("```{}```".format(output))
            except IndexError:
                await self.bot.say("Please enter a range between 2 and 9")

    @commands.command(pass_context=True)
    async def damage(self, ctx):
        """Display the formula for basic attack power."""
        try:
            await self.bot.send_typing(ctx.message.channel)
            await self.bot.upload(upload_folder + "\\" + "damage.png")
        except FileNotFoundError:
            await self.bot.upload(upload_folder + "\\" + "damage.jpg")

    @commands.command(pass_context=True)
    async def defense(self, ctx):
        """Display the formula for defense power."""
        await tools.uploadImage(self.bot, ctx, filename="defense")

    @commands.command(pass_context=True)
    async def fit2(self, ctx):
        """Display fit bonuses for cruisers."""
        await tools.uploadImage(self.bot, ctx, filename="fit2")

    @commands.command(pass_context=True)
    async def scratch(self, ctx):
        """Display the scratch damage formula."""
        await tools.uploadImage(self.bot, ctx, filename="scratch")

    @commands.command(pass_context=True)
    async def vanguard(self, ctx):
        """Display the modifiers for Vanguard (spoon) formation."""
        await tools.uploadImage(self.bot, ctx, filename="vanguard")

    @commands.command(pass_context=True)
    async def yasen(self, ctx):
        """Display the equipment setups for special night battle attacks."""
        await tools.uploadImage(self.bot, ctx, filename="yasen")

    @commands.command(pass_context=True)
    async def yasen2(self, ctx):
        """Display the equipment setups required for carrier night battle attacks."""
        await tools.uploadImage(self.bot, ctx, filename="yasen2")

    @commands.command(pass_context=True)
    async def aaci(self, ctx):
        """Display an AACI info chart."""
        await tools.uploadImage(self.bot, ctx, filename="aaci")

    @commands.command(pass_context=True)
    async def fit(self, ctx):
        """Displays overweight penalties and fit guns for battleships."""
        await tools.uploadImage(self.bot, ctx, filename="fit")

    @commands.command(pass_context=True)
    async def dgun(self, ctx):
        """Display 12.7cm D gun bonuses."""
        await tools.uploadImage(self.bot, ctx, filename="dgun")

    @commands.command(pass_context=True)
    async def greatsuccess(self, ctx):
        """Display great success chances for expeditions."""
        await tools.uploadImage(self.bot, ctx, filename="greatsuccess")

    @commands.command(pass_context=True)
    async def oasw(self, ctx):
        """Link to wikia OASW tables."""
        '''
        #async def oasw(self, ctx, *, kanmusu : str):
        oasw_database = tools.loadPickle('oasw_database.pickle')
        kanmusu = kanmusu.split(' ')[0].lower() # strip off any unnecessary tags (such as 'kai', 'kai ni', etc.)
        try:
            data = oasw_database[kanmusu]
        except KeyError:
            await self.bot.say("Unable to find **{}'s** data. Remember to use long sounds eg. _Y**uu**dachi_, not _Y**u**dachi_.".format(kanmusu[0].upper() + kanmusu[1:]))
            await oaswSuggestions(self.bot, ctx, kanmusu)
            return
        tags = oasw_database[len(oasw_database[kanmusu])]
        title = "{}'s Opening ASW data".format(kanmusu[0].upper() + kanmusu[1:])
        description = "Assuming highest kai'd form..."
        em = tools.createEmbed(title=title, description=description)
        for x in tags:
            em.add_field(name=x, value=data[tags.index(x)])
        await self.bot.say(embed=em)
        '''
        await self.bot.say("http://kancolle.wikia.com/wiki/Oasw")

    @commands.command()
    async def akashi(self):
        """Akashi's arsenal information (link to akashi-list)."""
        await self.bot.say('http://akashi-list.me')

    @commands.command()
    async def world(self, level : str):
        """View information for a specified map X-X."""
        if len(level) != 3 or level[1] != '-':
            await self.bot.say("Please do '!k.world N-N', where N is the world level.")
        else:
            field = (level[0], level[2])
            file_origin = paths.worldInfo()
            await self.bot.say("World {}-{} Map and branching rules:".format(field[0], field[1]))
            try:
                await self.bot.upload(file_origin + '\\{0}-{1}_Map.jpg'.format(field[0], field[1]))
            except Exception:
                try:
                    await self.bot.upload(file_origin + '\\{0}-{1}_Map.png'.format(field[0], field[1]))
                except Exception as e:
                    await self.bot.say("Unable to retrieve World {0}-{1} map info.".format(field[0], field[1]))
                    #await self.bot.say('{}: {}'.format(type(e).__name__, e))
            try:
                await self.bot.upload(file_origin + '\\{0}-{1}.png'.format(field[0], field[1]))
            except Exception:
                try:
                    await self.bot.upload(file_origin + '\\{0}-{1}.jpg'.format(field[0], field[1]))
                except Exception as e:
                    await self.bot.say("Unable to retrieve World {0}-{1} branching rules info.".format(field[0], field[1]))
                    #await self.bot.say('{}: {}'.format(type(e).__name__, e))
            try:
                nodes = staticData.airPower(int(field[0]), int(field[1]))
                data = 'Node/AS/AS+\n\n'
                for x in nodes:
                    data += "{0} - **{1}**, {2}\n".format(x, nodes[x][0], nodes[x][1])
                title = "{}-{} Air Superiority Requirements".format(field[0], field[1])
                em = tools.createEmbed(title=title, description=data)
                await self.bot.say(embed=em)
                #await self.bot.say('```Air superiority requirements\n{}```'.format(data))
            except Exception as e:
                await self.bot.say("Unable to display AS data.")
                #await self.bot.say('{}: {}'.format(type(e).__name__, e))

    '''
    @commands.command(pass_context=True)
    async def update(self, ctx, *, current_status : str):
        """Update the Kancolle Event Status Board with your current status.
        eg. `!k.update Clearing E5H`
        Only available on private server."""
        if not checks.check_hourai(ctx.message):
            return
        else:
            # Retrieve Kamikaze's message data
            message_id = "414614925978238988"
            event_channel = self.bot.get_channel("414474883360358410")
            status_message = await self.bot.get_message(channel=event_channel, id=message_id)

            # save current embed info
            em = status_message.embeds[0]
            new_em = tools.createEmbed(title="Event Status", description="What Admirals are currently doing in the event.\nUpdate yours with `!k.update <message>`.")
            try:
                users = [em["fields"][x]["name"] for x in range(len(em["fields"]))]
                user_values = [em["fields"][x]["value"] for x in range(len(em["fields"]))]
                data_exists = True
            except KeyError:
                data_exists = False

            if data_exists:
                if ctx.message.author.name in users:
                    # pop them if they're already on the list
                    kill_index = users.index(ctx.message.author.name)
                    users.pop(kill_index)
                    user_values.pop(kill_index)
            new_em.add_field(name=ctx.message.author.name, value=current_status)
            # recreate the embed using old embed data
            if data_exists:
                for user in users:
                    new_em.add_field(name=user, value=user_values[users.index(user)])
            # edit the message
            await self.bot.edit_message(message=status_message, embed=new_em)
            await self.bot.say("Updated your current event status!")
    '''

    '''
    @commands.command(pass_context=True)
    async def medals(self, ctx, *, map_difficulties : str):
        """Update the Kancolle Event Medal Tally with your current clears.
        eg. `!k.medals HHCEMHH`
        Use `!k.medals x` to clear your medal list.
        Only available on private server."""
        if not checks.check_hourai(ctx.message):
            return
        else:
            event_length = 7
            message_id = "414827581624549386"
            event_channel = self.bot.get_channel("414474883360358410")
            medal_message = await self.bot.get_message(channel=event_channel, id=message_id)

            # save current embed info
            em = medal_message.embeds[0]
            new_em = tools.createEmbed(title="Difficulty Clear Status", description="Event medals that Admirals have currently obtained.\nUpdate yours with `!k.medals <medal string/eg.HHHMME>`\nYou can clear with `!k.medals x`.")
            try:
                users = [em["fields"][x]["name"] for x in range(len(em["fields"]))]
                user_values = [em["fields"][x]["value"] for x in range(len(em["fields"]))]
                data_exists = True
            except KeyError:
                data_exists = False

            # dictionary translations
            parse = {
                "C" : "<:EventMedalCasual:414828756130070529>",
                "E" : "<:EventMedalEasy:414829530910425108>",
                "M" : "<:EventMedalNormal:414829531283849227>",
                "N" : "<:EventMedalNormal:414829531283849227>",
                "H" : "<:EventMedalHard:414829531334180884>",
                "X" : ":no_entry_sign:"
            }

            # parse difficulty string
            map_difficulties = map_difficulties.upper().replace(' ','').replace(',','')
            if len(map_difficulties) > event_length:
                await self.bot.say("That's more than 7 medals there. Please look it over and try again.")
                return
            parsed_str = ""
            for x in map_difficulties:
                if x not in ['C','E','M','N','H','X']:
                    await self.bot.say("Hmmm, I can't translate that to medals. Try `C`, `E`, `M/N`, and `H`.")
                    return
                parsed_str += parse[x]

            if data_exists:
                if ctx.message.author.name in users:
                    # pop them if they're already on the list
                    kill_index = users.index(ctx.message.author.name)
                    users.pop(kill_index)
                    user_values.pop(kill_index)
            new_em.add_field(name=ctx.message.author.name, value=parsed_str)
            # recreate the embed using old embed data
            if data_exists:
                for user in users:
                    new_em.add_field(name=user, value=user_values[users.index(user)])
            # edit the message
            await self.bot.edit_message(message=medal_message, embed=new_em)
            await self.bot.say("Updated your event medal tally!")
    '''

def setup(bot):
    bot.add_cog(Kancolle(bot))
