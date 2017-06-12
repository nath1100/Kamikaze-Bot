import discord
from discord.ext import commands
try:
    import cPickle as pickle
except ImportError:
    import pickle

def loadPickle(file : str):
    with open(file, 'rb') as f:
        data = pickle.load(f)
    return data

def dumpPickle(data, file : str):
    with open(file, 'wb') as f:
        pickle.dump(data, f)

def createEmbed(title, description=None):
    return discord.Embed(title=title, description=description, color=14031172)

def gainCoins(target, amount : int):
    with open('coin_stash.pickle', 'rb') as f:
        coin_stash = pickle.load(f)
    try:
        coin_stash[target.id] += amount
    except KeyError:
        coin_stash[target.id] = amount
    with open('coin_stash.pickle', 'wb') as f:
        pickle.dump(coin_stash, f)

def findMember(bot, member_id : str):
    """Looks in each server and returns a member if found."""
    for server in bot.servers:
        member = server.get_member(member_id)
        if member is not None:
            return member 

async def inputTimeout(bot, ctx, topic : str):
    await bot.send_message(ctx.message.channel, "{}, your {} has timed out".format(ctx.message.author.mention, topic))
