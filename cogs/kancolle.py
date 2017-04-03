import asyncio, discord, datetime, random
from discord.ext import commands
from cogs.utilities import paths, staticData
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

    @commands.group(pass_context=True)
    async def doomsday(self, ctx):
        """Doomsday counter counting down to something"""
        try:
            target, flavour_text = doomsday_target[0], doomsday_target[1]
            await self.bot.say('Retrieved time data from local scope. (aka, you have trascended time and space and torn through the fabric of space time know as "scope"...)')
        except NameError:
            with open('doomsday_target.pickle', 'rb') as f:
                doomsday_target = pickle.load(f)
            target, flavour_text = doomsday_target[0], doomsday_target[1]
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

    @doomsday.command()
    async def edit(self, year : int, month : int, day : int, hour : int, minute : int, second : int, flavour_text : str):
        """Edits the target date of the doomsday command"""
        doomsday_target = [datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second), flavour_text]
        try:
            with open('doomsday_target.pickle', 'wb') as f:
                pickle.dump(doomsday_target, f)
            await self.bot.say('Successfully updated the doomsday target!')
        except Exception:
            await self.bot.say('Uh oh, something went wrong... PM an admin.')

    @commands.group(pass_context=True)
    async def lbas(self, ctx):
        """Contains various LBAS tools"""
        if ctx.invoked_subcommand is None:
            await self.bot.say('No such topic found. Use !k.help lbas for a list.')

    @lbas.command()
    async def range_bonus(self, plane=''): # PLEASE REWORK THIS, IT'S CANCEROUS TO LOOK AT
        """Displays LBAS scout bonus chart"""
        data = 'Shortest Range | Range Bonus\n'
        if plane == '':
            await self.bot.upload(upload_folder + '\\' + 'lbas_scout_bonus.png')
        elif plane.lower() == 'type2 large flying boat' or 'taitei' in plane.lower() or 'boat' in plane.lower():
            for x in range(2, 10):
                data += '\t\t%s\t\t\t+3\n' % x
                self.bot.say('```%s```' % data)
        elif 'catalina' in plane.lower():
            for x in range(2, 4):
                data += '\t\t%s\t\t\t+3\n' % x
            for x in range(4, 8):
                data += '\t\t%s\t\t\t+2\n' % x
            for x in range(8, 10):
                data += '\t\t%s\t\t\t+1\n' % x
        elif 'keiun' in plane.lower() or 'saiun' in plane.lower():
            for x in range(2, 6):
                data += '\t\t%s\t\t\t+2\n' % x
            for x in range(6, 8):
                data += '\t\t%s\t\t\t+1\n' % x
            for x in range(8, 10):
                data += '\t\t%s\t\t\t+0\n' % x
        elif 'type0' in plane.lower():
            for x in range(2, 5):
                data += '\t\t%s\t\t\t+2\n' % x
            for x in range(5, 7):
                data += '\t\t%s\t\t\t+1\n' % x
            for x in range(7, 10):
                data += '\t\t%s\t\t\t+0\n' % x
        elif 'type2' in plane.lower():
            data += '\t\t2\t\t\t+2\n'
            for x in range(3, 5):
                data += '\t\t%s\t\t\t+1\n' % x
            for x in range(5, 10):
                data += '\t\t%s\t\t\t+0\n' % x
        else:
            await self.bot.say('Invalid scout aircraft')
            return
        if plane != '':
            await self.bot.say('```{}```'.format(data))


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