
''' SHELVED INDEFINITELY

import discord
from discord.ext import commands
from cogs.utilities import checks

def evaluate(message, text : str):
    """rewrite code"""
    code = text.replace('print(', 'self.bot.send_message({}, '.format(message.channel))
    return code

class Repl:
    """Kamikaze REPL; get kamikaze to execute code"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def execute(self, ctx, *, content):
        """Kamikaze executes a 1 line python code (have fun)"""
        if checks.check_owner(ctx.message):
            try:
                await exec(evaluate(ctx.message, content))
            except Exception as e:
                self.bot.say("{}: {}".format(type(e).__name__, e))


def setup(bot):
    bot.add_cog(Repl(bot))

'''