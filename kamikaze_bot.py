import asyncio, discord, logging, os
from discord.ext import commands
from cogs.utilities import tools
try:
    import cPickle as pickle
except ImportError:
    import pickle

#Initialisations
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

def get_key():
    creds = tools.loadPickle("crds.pickle")
    with open(creds['keyPath'], "r") as f:
        key = f.read()
    return key

token = get_key()

version = '1.0.2.6'

extension_list = [
    'cogs.loader',
    'cogs.admin',
    'cogs.generic',
    'cogs.kancolle',
    'cogs.keywords',
    'cogs.internet',
    'cogs.nsfw',
    'cogs.wows',
    'cogs.soku',
    'cogs.extras',
    'cogs.music',
    'cogs.sinoalice'
]

description = """Super cute Kamikaze will attend to your KC needs."""
bot = commands.Bot(command_prefix='!k.', description=description)
bot.remove_command('help')

with open('oasw_database.pickle', 'rb') as f:
    oasw_database = pickle.load(f)

#constants
upload_folder = "upload_command_files" #cogs generic, kancolle

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('Home located in: ' + os.getcwd())
    print('Version ' + version) ####### VERSION NUMBER
    print('------')
    with open('kamikaze_status.pickle', 'rb') as f:
        kamikaze_status = pickle.load(f)
    await bot.change_presence(game=discord.Game(name=kamikaze_status[0]))


@bot.command(hidden=True)
async def get_version():
    """Checks the version of kamikaze"""
    await bot.say('This is version: **{}**'.format(version))

@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.MissingRequiredArgument):
        await bot.send_message(ctx.message.channel, "Did you forget a parameter?")
    elif isinstance(error, commands.CommandNotFound):
        #await bot.send_message(ctx.message.channel, "That command does not exist. Try !k.help")
        pass # let command fail silently
    elif isinstance(error, commands.NoPrivateMessage):
        await bot.send_message(ctx.message.channel, "This command cannot be used in private message.")
    else:
        error_m = await bot.send_message(ctx.message.channel, "Eeh!? Something has gone very wrong!  ∑(O_O;) \nPlease be patient until this is fixed~!")
        try:
            await bot.send_message(ctx.message.server.get_member(user_id='178112312845139969'), "{} in {}: <{}>\nError: {}".format(ctx.message.author, ctx.message.server, ctx.message.content, error))
        except AttributeError:
            # do not send error reports for PMs
            pass

#admin and other
@bot.event
async def on_message(message):

    if message.author == bot.user:
        return
    await bot.process_commands(message)

if __name__ == '__main__':
    for extension in extension_list:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print('Unable to load extension')
            print(type(e))
            print(e)

@bot.event
async def on_server_join(server):
    # Do something
    pass

bot.run(token)
