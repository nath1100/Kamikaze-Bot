import discord
from discord.ext import commands
try:
    import cPickle as pickle
except ImportError:
    import pickle

## Permissions checks (pass message)
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

def check_hourai(message):
    return message.server.id == "260977178131431425"

# Channel ID checks (pass message)
def check_soku(message):
    return message.channel.id == '271935186151669774'

def check_nsfw(message):
    try:
        return message.channel.name == "nsfw" or message.channel.name.startswith("nsfw-")
    except AttributeError: # name is None
        return message.channel.is_private

## Type checks
def convertsToInt(obj):
    try:
        int(obj)
        return True
    except ValueError:
        return False
