import discord, os
from discord.ext import commands
from cogs.utilities import paths, checks
from datetime import datetime, date, time

class Sinoalice:
    """Various commands related to mobile game SINoALICE."""

    def __init__(self, bot):
        self.bot = bot
        self.uploadFolder = paths.sinoaliceInfo()

    @commands.command()
    async def regen(self, current_AP : str, end_time : str):
        """Calculate the amount of AP regenerated specifying current AP and a target time.
        End_time format should be HH:MM, eg 06:00 or 23:41."""
        try:
            current_AP = int(current_AP)
            hour, minute = end_time.split(":")
        except ValueError:
            await self.bot.say("`<current_AP>` should be integer and `<end_time>` should be HH:MM 24 hour time.")
            return
        if not checks.convertsToInt(hour) and checks.convertsToInt(minute):
            await self.bot.say("`End_time` should be a 24 hour time in format HH:MM.")
        else:
            timeLeft = datetime.combine(date.min, time(hour=int(hour), minute=int(minute))) - datetime.combine(date.min, datetime.time(datetime.now()))
            seconds = timeLeft.total_seconds()
            if seconds < 0:
                await self.bot.say("`End_time` cannot be in the past! @ ~ @;")
                return
            await self.bot.say("You will have **{}** AP by {}".format(int(seconds/180) + current_AP, end_time))

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
