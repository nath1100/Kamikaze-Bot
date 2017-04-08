import asyncio, discord, datetime, random
from discord.ext import commands
from cogs.utilities import paths, staticData, tools
try:
    import cPickle as pickle
except ImportError:
    import pickle

#constants
upload_folder = paths.uploadFolder()

class Kancolle:
    """Commands related to Kancolle stuff"""

    def __init__(self, bot):
        self.bot = bot

    '''
    @commands.group(pass_context=True)
    async def doomsday(self, ctx):
        """Doomsday counter counting down to something"""
        serverID = ctx.message.server.id
        doomsday_target = tools.loadPickle('doomsday_target.pickle')
        target = doomsday_target[serverID][0]
        flavour_text = doomsday_target[serverID][1]

        time_left = target - datetime.datetime.now()
        if ((time_left.days*24*60*60) + time_left.seconds) < 0:
            time_left = datetime.datetime(2222, 9, 25, 0, 0, 0) - datetime.datetime.now()
            random_flavour_text = ['kittens fly', 'One Piece ends', 'Eva refloats her rightful ship', 'Samidare Kai Ni', 'Sims gets proper torpedoes',
                'Gremyaschy gets nerfed', 'we run out of salt', 'HotD season 2', 'Shinomiya wins', 'Shirogane wins', 'Ishigami overcomes his fear of Shinomiya',
                'Suzukaze Kai Ni', 'Gisele Alain comes off haitus', 'Mizuki awakens to his inner self', 'the Abyssals win the war', 'future bass becomes present bass',
                'Kamikaze turns 300', '2017 winter E-3 debuff confirmed']
            flavour_text = 'until ' + random.choice(random_flavour_text)
        seconds_left = time_left.seconds + (time_left.days*24*60*60)
        mins, seconds = divmod(seconds_left, 60)
        hrs, minutes = divmod(mins, 60)
        days, hours = divmod(hrs, 24)
        if ctx.message.content == '!k.doomsday':
            await self.bot.say('**{} days, {} hours, {} minutes and {} seconds {}**'.format(days, hours, minutes, seconds, flavour_text))

    @doomsday.command(pass_context=True)
    async def edit(self, ctx, year : int, month : int, day : int, hour : int, minute : int, second : int, *, flavour_text : str):
        """Edits the target date of the doomsday command"""
        serverID = ctx.message.server.id
        doomsday_target = tools.loadPickle('doomsday_target.pickle')
        doomsday_target[serverID] = [datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second), flavour_text]
        try:
            tools.dumpPickle(doomsday_target, 'doomsday_target.pickle')
            await self.bot.say('Successfully updated the doomsday target!')
        except Exception as e:
            await self.bot.say('Uh oh, something went wrong... PM an admin.')
            await self.bot.say("{}: {}.format(type(e).__name__, e)")
    '''

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
    @commands.command()
    async def oasw(self, kanmusu : str):
        """Searches oasw lvl requirements of kanmusu"""
        ## integrate into checks
        with open('oasw_database.pickle', 'rb') as f:
            oasw_database = pickle.load(f)
        ##
        kanmusu = kanmusu.strip("'\"")
        try:
            length = len(oasw_database[kanmusu.lower()]) # optimise the try/exception block later
        except KeyError:
            if kanmusu + ' kai' in oasw_database:
                kanmusu += ' kai'
                length = len(oasw_database[kanmusu.lower()])
            elif kanmusu + ' kai ni' in oasw_database:
                kanmusu += ' kai ni'
                length = len(oasw_database[kanmusu.lower()])
            else:
                await self.bot.say("Sorry, couldn't find her in the database.")
                return
        await self.bot.say('OASW lvl requirements for ' + kanmusu)
        counter = 0
        result = ''
        if length == 11:
            tags = ['T4/T4/T4', 'T4/T4/T3', 'T4/T4/DC', 'T4/T3/DC', 'T3/T3/DC', 'T4/T4', 'T4/T3', 'T4/DC', 'T3/DC', 'T4', 'T3']
        elif length == 17:
            tags = ['T4/T4/T4/T4', 'T4/T4/T4/T3', 'T4/T4/T4/DC', 'T4/T4/T3/DC', 'T4/T3/T3/DC', 'T3/T3/T3/DC', 'T4/T4/T4', 'T4/T4/T3', 'T4/T4/DC', 'T4/T3/DC', 'T3/T3/DC', 'T4/T4', 'T4/T3', 'T4/DC', 'T3/DC', 'T4', 'T3']
        for x in tags:
            result += (x + ': ' + str(oasw_database[kanmusu.lower()][counter]) + '\n')
            counter += 1
        await self.bot.say('```{}```'.format(result))

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
                    await self.bot.say('{}: {}'.format(type(e).__name__, e))
            try:
                await self.bot.upload(file_origin + '\\{0}-{1}.png'.format(field[0], field[1]))
            except Exception:
                try:
                    await self.bot.upload(file_origin + '\\{0}-{1}.jpg'.format(field[0], field[1]))
                except Exception as e:
                    await self.bot.say("Unable to retrieve World {0}-{1} branching rules info.".format(field[0], field[1]))
                    await self.bot.say('{}: {}'.format(type(e).__name__, e))
            try:
                nodes = staticData.airPower(int(field[0]), int(field[1]))
                data = ''
                for x in nodes:
                    data += "{0} - AS {1}, {2}\n".format(x, nodes[x][0], nodes[x][1])
                await self.bot.say('```Air superiority requirements\n{}```'.format(data))
            except Exception as e:
                await self.bot.say("Unable to display AS data.")
                await self.bot.say('{}: {}'.format(type(e).__name__, e))


def setup(bot):
    bot.add_cog(Kancolle(bot))