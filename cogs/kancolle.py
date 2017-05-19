import asyncio, discord, random, datetime, shelve
from discord.ext import commands
from cogs.utilities import paths, staticData, tools
try:
    import cPickle as pickle
except ImportError:
    import pickle

#constants
upload_folder = paths.uploadFolder()

async def oaswSuggestions(bot, ctx, kanmusu):
    kanmusu = kanmusu.lower()
    if kanmusu == 'hibiki':
        suggestion = 'Verniy, Bep'
        await bot.send_message(ctx.message.channel, "Perhaps you meant _{}_".format(suggestion))

class Kancolle:
    """Commands related to Kancolle stuff"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def compareships(self, ctx, *, args : str):
        """Enter two comma separated kanmusu to compare their stats."""
        try:
            firstShip, secondShip = args.split(', ')
        except ValueError:
            await self.bot.say("Did you forget to put a **comma** and **space** (`ship1, ship2`) or did you put too many?")
            return
        with shelve.open("db\\ship_db", "r") as shelf:
            try:
                ship1 = shelf[firstShip.lower()]
            except KeyError:
                await self.bot.send_message(ctx.message.channel, "Unable to find **{}**.".format(firstShip))
                return
            try:
                ship2 = shelf[secondShip.lower()]
            except KeyError:
                await self.bot.send_message(ctx.message.channel, "Unable to find **{}**.".format(secondShip))
                return
        if ship1 is None or ship2 is None:
            return
        else:
            #build the embed
            firstShipFormatted, secondShipFormatted = firstShip[0].upper() + firstShip[1:].lower(), secondShip[0].upper() + secondShip[1:].lower()
            title = "{}'s stats VS {}".format(firstShipFormatted, secondShipFormatted)
            description = "Comparing max stats (except luck)"
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
                ('ammo', 'Ammo Consumption')
            ]
            for stat in stats:
                if ship1[stat[0]] == -1 or ship2[stat[0]] == -1:
                    statResult = 'No Data'
                else:
                    statResult = ship1[stat[0]] - ship2[stat[0]]
                    if statResult > 0:
                        statResult = "**+{}**".format(statResult)
                em.add_field(name=stat[1], value=statResult)
            await self.bot.say(embed=em)

    @commands.command(pass_context=True)
    async def lbasRange(self, ctx, shortest_range : int):
        """Display LBAS range bonuses given the lowest aircraft range"""
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
        """Displays an AACI chart"""
        await self.bot.upload(upload_folder + '\\' + 'aaci.png')

    @commands.command()
    async def fit(self):
        """Displays overweight penalties and fit guns for battleships"""
        await self.bot.upload(upload_folder + '\\' + 'fit.png')

    #### REQUIRES REWORK ####
    @commands.command(pass_context=True)
    async def oasw(self, ctx, *, kanmusu : str):
        """Searches oasw lvl requirements of kanmusu"""
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
        """Akashi's arsenal information"""
        await self.bot.say('http://akashi-list.me')

    @commands.command()
    async def world(self, level : str):
        """View world information"""
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