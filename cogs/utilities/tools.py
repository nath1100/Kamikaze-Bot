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

def createEmbed(title, description):
    return discord.Embed(title=title, description=description, color=14031172)

def gainCoins(target, amount : int):
    coin_stash = tools.loadPickle('coin_stash.pickle')
    try:
        coin_stash[target.id] += amount
    except KeyError:
        coin_stash[target.id] = amount
    with open('coin_stash.pickle', 'wb') as f:
        pickle.dump(coin_stash, f)