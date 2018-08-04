import discord, requests
from discord.ext import commands
from cogs.utilities import tools
from bs4 import BeautifulSoup

def getData(gun : str):
    # Retrieve data from the en GFL wiki.
    page = requests.get("https://en.gfwiki.com/wiki/{}".format(gun))
    if page.status_code == 404:
        # No page was found, so return type : None
        return
    else:
        soup = BeautifulSoup(page.text, "html.parser")
        # Retrieve the table containing T-Doll's stats
        statTable = soup.find(class_="verticaltabber paddedtabber-2px costumeContainer stattable")
        # The attribute used to ID the data.
        attribute = "data-tdoll-stat-id"
        stats = {
            "Health" : ["span", "max_hp_t"],
            "5xLinked Health" : ["span", "hpmaxwd"],
            "Damage" : ["td", "max_dmg_t"],
            "Evasion" : ["td", "max_eva_t"],
            "Accuracy" : ["td", "max_acc_t"],
            "RoF" : ["td", "max_rof_t"],
            "Move Speed" : ["td", "mov_t"]
        }
        # Compile the resultant stats into results : dict
        results = {}
        for stat in stats:
            tag, attr = stats[stat]
            results[stat] = statTable.find(tag, {attribute : attr}).contents[0]
        return results

def parseGuns(gun_string : str):
    # Receive gunString and return adequately parsed guns
    if "," not in gun_string:
        return (gun_string, None)
    else:
        # Split into two variables, gun1 and gun2, taking into account comma habits.
        try:
            gun1, gun2 = gun_string.split(", ")
        except ValueError:
            gun1, gun2 = gun_string.split(",")
        # Replace spaces with underscores
        for g in [gun1, gun2]:
            g.replace(" ","_")
        return gun1, gun2

class Girlsfrontline:
    """Various commands for the mobile game GIRLS' FRONTLINE."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, aliases=["comparegun", "comapareguns", "comapreguns", "comapregun"])
    async def compareguns(self, ctx, *, guns : str):
        """Compare or lookup the stats of various T-Dolls.
        Compare by doing `!k.compareguns gun1, gun2` and lookup by using `!k.compareguns gun`."""
        # Parse the guns string
        gun1, gun2 = parseGuns(guns)
        # Get data (: dict) of first gun
        await self.bot.send_typing(ctx.message.channel)
        gun1_data = getData(gun1)
        # Check for Error 404
        if gun1_data is None:
            # It was 404, suggest comma checks if they werent present but spaces were.
            if all([x in guns for x in [",", " "]]):
                suggestion = " Perhaps you left out the comma?"
            else:
                suggestion = ""
            await self.bot.say("Unable to find **{}**. Please check your spelling.{}")
        # Check if this is a lookup or a compare by checking if gun2 is type : None
        if gun2 is None:
            gun2_data = {
                "Health" : "0",
                "5xLinked Health" : "0",
                "Damage" : "0",
                "Evasion" : "0",
                "Accuracy" : "0",
                "RoF" : "0",
                "Move Speed" : "0"
            }
            title = "{}'s stats".format(gun1)
            desc = "Viewing max stats"
        else:
            gun2_data = getData(gun2)
            title = "{}'s stats VS {}'s stats".format(gun1, gun2)
            desc = "Comparing max stats"
        # Create the Embed
        em = tools.createEmbed(title, desc)
        # Loop over the stats dict and add
        for stat in gun1_data:
            val = int(gun1_data[stat]) - int(gun2_data[stat])
            if val > 0 and gun2 is not None:
                # If positive value, bolden the number.
                em.add_field(name=stat, value="**{}**".format(val))
            else:
                em.add_field(name=stat, value=val)
        # Finally, output the embed.
        await self.bot.say(embed=em)

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
