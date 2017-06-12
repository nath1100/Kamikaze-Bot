import discord, random
from discord.ext import commands
from cogs.utilities import checks, tools

class Keywords:
    """Special commands that trigger responses from Kamikaze."""

    def __init__(self, bot):
        self.bot = bot

    async def on_message(self, message):
        if message.author == self.bot.user or message.author.bot:
            return
        else:
            if 'marry me kamikaze' == message.content.lower():
                if checks.check_owner(message): #if you're mintea:
                    response = random.choice(['Fuck off.', 'Shut up you bastard.', 'Kill yourself.', "Why don't you go jerk off to Asanagi, you Kuso."])
                else: #otherwise, if you're not mintea:
                    if random.randint(1, 10000) == 1: #roll 0.01% chance for happy end
                        await self.bot.send_message(message.channel, random.choice('Sure~ <3', 'Ok ///w///'))
                    else: #otherwise, get a response from the accumulated rejection list
                        response_choices = ['No thanks~', 'Eh? uh.. sorry.', 'Marriage? Eh.. sorry.', 'M-Marriage? Uh.. maybe not.',
                            'Marriage? Don\'t you have more important duties to attend to?', 'Maybe when you\'re a little older...',
                            'The age gap though... Sorry.']
                        if message.author.id == '172704013911982080': #if you're Jimmy:
                            more_choices = ['But you have Kawakaze...', 'But you\'re already married to Kongou...', 'If you had a girlfriend, you wouldn\'t need to constantly propose to me.', 'If you had a girlfriend, I wouldn\'t have to constantly reject you.']
                        elif message.author.id == '176610457992429568': #if you're nyanko:
                            more_choices = ['But you have Bep...']
                        try:
                            for x in more_choices:
                                response_choices.append(x)
                        except Exception:
                            pass
                        response = random.choice(response_choices)
                await self.bot.send_message(message.channel, response)

            elif 'shutup kamikaze' in message.content.lower():
                switch = tools.loadPickle('kamikaze_chime.pickle')
                switch[message.server.id] = False
                tools.dumpPickle(switch, 'kamikaze_chime.pickle')
                await self.bot.send_message(message.channel, 'Sorry... ; A ;')

            elif 'sorry kamikaze' in message.content.lower():
                switch = tools.loadPickle('kamikaze_chime.pickle')
                switch[message.server.id] = True
                tools.dumpPickle(switch, 'kamikaze_chime.pickle')
                await self.bot.send_message(message.channel, 'u w u')

            elif 'kamikaze' in message.content.lower():
                switch = tools.loadPickle('kamikaze_chime.pickle')
                try:
                    if switch[message.server.id]:
                        interruption = ['Did someone call me? :D', 'Someone say my name?']
                        await self.bot.send_message(message.channel, random.choice(interruption))
                        msg = await self.bot.wait_for_message(timeout=5, author=message.author, check=lambda x: x.content.lower() in ['yes', 'no', 'help'])
                        try:
                            if 'yes' in msg.content.lower():
                                await self.bot.send_message(message.channel, 'o w o')
                            elif 'no' in msg.content.lower():
                                await self.bot.send_message(message.channel, '> _ <')
                            elif 'help' in msg.content.lower():
                                await self.bot.send_message(message.channel, "Say !k.help for a list of commands = w =")
                        except AttributeError:
                            pass
                except KeyError:
                    await self.bot.send_message(message.channel, "No server info detected. Please run _serverSetup command.")
                except AttributeError:
                    pass

def setup(bot):
    bot.add_cog(Keywords(bot))