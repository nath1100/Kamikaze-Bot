import asyncio, discord, random, datetime, shelve
from discord.ext import commands
from cogs.utilities import paths, staticData, tools
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
                ('base_lvl', 'Base Level')
            ]
            for stat in stats:
                if ship1[stat[0]] == -1 or ship2[stat[0]] == -1:
                    statResult = 'No Data'
                else:
                    statResult = ship1[stat[0]] - ship2[stat[0]]
                    if statResult > 0 and secondShip != ZERO_STAT_COMPARATOR:
                        statResult = "**+{}**".format(statResult)
                em.add_field(name=stat[1], value=statResult)
            await self.bot.say(embed=em)

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

    @commands.command()
    async def aaci(self):
        """Display an AACI info chart."""
        await self.bot.upload(upload_folder + '\\' + 'aaci.png')

    @commands.command()
    async def fit(self):
        """Displays overweight penalties and fit guns for battleships."""
        await self.bot.upload(upload_folder + '\\' + 'fit.png')

    @commands.command(pass_context=True)
    async def oasw(self, ctx, *, kanmusu : str):
        """Show the OASW level requirements for a kanmusu."""
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

def setup(bot):
    bot.add_cog(Kancolle(bot))
