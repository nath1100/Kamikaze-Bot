import discord
from discord.ext import commands
from cogs.utilities import tools

class Girlsfrontline:
    """Various commands for game Girls Frontline."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["gflformulas", "gflf"])
    async def gflFormulas(self):
        """Display the basic combat forumals for GFL."""
        em = tools.createEmbed(title="GFL Combat Formulas")
        formulas = {
            "Evasion" : "hit_rate = 1 - (evasion / (evasion + enemy_acc))",
            "Equipment/Skill/Tile" : "(Base Stat + Equip) * (Skill 1) * (Skill 2) * (Tile Buff + Tile Buff)"
        }
        for formula in formulas:
            em.add_field(name=formula, value="`{}`".format(formulas[formula]))
        await self.bot.say(embed=em)

def setup(bot):
    bot.add_cog(Girlsfrontline(bot))
