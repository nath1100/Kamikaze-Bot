import discord, os
from discord.ext import commands
from cogs.utilities import paths

class Sinoalice:
    """Various commands related to mobile game SINoALICE."""

    def __init__(self, bot):
        self.bot = bot
        self.uploadFolder = paths.sinoaliceInfo()

    @commands.command(pass_context=True)
    async def menu(self, ctx, *, menu_page=None):
        """View translated SINoALICE menus."""
        if menu_page is None:
            await self.bot.say("pass")
            await menuNavigation()
        elif menu_page == "list":
            await self.bot.say('```{}```'.format(', '.join([x[:-4] for x in os.listdir(self.uploadFolder)])))
        else:
            await self.bot.send_typing(ctx.message.channel)
            try:
                await self.bot.upload(self.uploadFolder + "\\{}.jpg".format(menu_page))
            except FileNotFoundError:
                try:
                    await self.bot.upload(self.uploadFolder + "\\{}.png".format(menu_page))
                except FileNotFoundError:
                    await self.bot.say("No such menu translation found. `!k.menu list` for a list, or `!k.menu` for navigation.")


def setup(bot):
    bot.add_cog(Sinoalice(bot))
