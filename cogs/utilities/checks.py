import discord
from discord.ext import commands
try:
    import cPickle as pickle
except ImportError:
    import pickle

# Permissions checks (pass message)
# Houraigekisen specific. Not a real administrator check.
def check_teitoku(message):
    return message.author.top_role.name == 'Teitoku'

# Bot owner, not server owner.
def check_owner(message):
    return message.author.id == '178112312845139969'

def check_admin(message):
    return message.channel.permissions_for(message.author).administrator

def check_moderator(message):
    return message.channel.permissions_for(message.author).manage_messages


# Channel ID checks (pass message)
def check_soku(message):
    return message.channel.id == '271935186151669774'

def check_nsfwEnabled(message):
    with open('nsfwChannels.pickle', 'rb') as f:
        ch_list = pickle.load(f)
    return message.channel.id in ch_list