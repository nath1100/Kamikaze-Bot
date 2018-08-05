import discord, aiohttp
from discord.ext import commands
from cogs.utilities import tools
from bs4 import BeautifulSoup

async def getData(gun : str):
    """Retrieve stat data for a T-Doll from en GFL wiki"""
    async with aiohttp.get("https://en.gfwiki.com/wiki/{}".format(gun)) as page:
        if page.status == 404:
            # No page was found, so return type : None
            return
        else:
            soup = BeautifulSoup(await page.text(), "html.parser")
            # Retrieve the table containing T-Doll's stats
            stat_table = soup.find(class_="verticaltabber paddedtabber-2px costumeContainer stattable")
            new_formatting = False
            # Check for the "new" table formatting if old table format doesn't exist
            if stat_table is None:
                stat_table = soup.find(class_="upgradeablestattable")
                new_formatting = True
            # Check if the page given is a valid T-Doll page.
            if stat_table is None:
                return
            else:
                # The attribute used to ID the data.
                attribute = "data-tdoll-stat-id"
                stats = {
                    "Health" : ["span", "max_hp" if new_formatting else "max_hp_t"],
                    "5xLinked Health" : ["span", "hpmaxwd"],
                    "Damage" : ["td", "max_dmg" if new_formatting else "max_dmg_t"],
                    "Evasion" : ["td", "max_eva" if new_formatting else "max_eva_t"],
                    "Accuracy" : ["td", "max_acc" if new_formatting else "max_acc_t"],
                    "RoF" : ["td", "max_rof" if new_formatting else "max_rof_t"],
                    "Move Speed" : ["td", "mov" if new_formatting else "mov_t"],
                    "Crit Rate" : ["td", "crit" if new_formatting else "crit_t"],
                    "Crit Damage" : ["td", "critdmg" if new_formatting else "critdmg_t"]
                }
                # Compile the resultant stats into results : dict
                results = {}
                for stat in stats:
                    tag, attr = stats[stat]
                    # If the stat has a percent sign, remove it
                    if stat in ["Crit Rate", "Crit Damage"]:
                        results[stat] = stat_table.find(tag, {attribute : attr}).contents[0].replace("%","")
                    else:
                        results[stat] = stat_table.find(tag, {attribute : attr}).contents[0]
                # Retrieve the T-Doll's tileset data, taking into account new and old formatting
                if new_formatting:
                    tile_table = stat_table.find(class_="tilegridtable")
                else:
                    tile_table = stat_table.find("table", {"style" : "background: rgba(0, 0, 0, 0.25);padding:10px", "cellpadding" : "15%"})
                # Get the tileset 3x3 squares (from left to right, top to bottom)
                raw_tile_set = tile_table.find_all("td")
                tile_set = [tile.prettify().replace("\n","") for tile in raw_tile_set]
                # Translate tile colours, taking into account new and old formatting
                for tile in tile_set:
                    if ("<td></td>" if new_formatting else "background:rgba(0, 0, 0, 0.5)") in tile:
                        tile_set[tile_set.index(tile)] = ":black_circle:"
                    elif ('class="buff"' if new_formatting else "background:rgba(0, 255, 222, 1)") in tile:
                        tile_set[tile_set.index(tile)] = ":large_blue_circle:"
                    else:
                        tile_set[tile_set.index(tile)] = ":white_circle:"
                # Retrieve the T-Doll's tile buff (formatting is the same for old and new)
                tile_buff_bar = stat_table.find("div", {"style" : "background:rgba(0, 0, 0, 0.5);vertical-align:top;text-align:left;padding:15px;margin:5px;flex-grow:1"})
                # Parse three lines of data: Affects X, Buff 1, Buff 2 (take new (aura{}) and old (aura{}_t) formatting into account)
                try:
                    buffs = [tile_buff_bar.find("div", {"data-tdoll-stat-id" : "aura{}".format(x) if new_formatting else "aura{}_t".format(x)}).contents[0] for x in range(1, 4)]
                except IndexError:
                    # T-Doll only has 1 buff (so 2 lines, not 3)
                    buffs = [tile_buff_bar.find("div", {"data-tdoll-stat-id" : "aura{}".format(x) if new_formatting else "aura{}_t".format(x)}).contents[0] for x in range(1, 3)]
                # If the doll is an HG, append stat data (as stat data is separated from label data)
                if all([x.endswith(" ") for x in buffs[1:]]):
                    # Parse the div tags holding the linked doll stats for HGs and append them to the buff list
                    raw_buff_stats = tile_buff_bar.find_all("div", {"style" : "width:100%;text-align:right"})
                    # Prettify and remove sub tags, newlines, and double spaces
                    buff_stats = [buff.prettify().replace("<sub>","").replace("</sub>","").replace("\n","").replace("  "," ") for buff in raw_buff_stats]
                    # Further remove div tags and double spacing
                    buff_stats = [buff.replace("  "," ").replace('<div style="width:100%;text-align:right"> ','').replace(" </div>","") for buff in buff_stats]
                    # Append the cleaned buffs to the original buff list. buffs[x+1] because index 0 is not a buff.
                    for x in range(0, len(buffs) - 1):
                        buffs[x + 1] = buffs[x + 1] + buff_stats[x]
                # Add the tile buff data and tile grid to the results dict
                results["Tile Buff"] = buffs
                results["Tile Grid"] = tile_set
                # Retrieve T-Doll portrait, taking new and old formatting into consideration
                if new_formatting:
                    profile_card = soup.find(class_="floatright profiletable")
                    img_tag = profile_card.find("img")
                    image_url = img_tag.get("src")
                else:
                    profile_card = soup.find(class_="card-bg")
                    imgs = [img.get("src") for img in profile_card.find_all("img")]
                    for img in imgs:
                        if gun in img:
                            image_url = img
                # Add the image URL to the results dict
                results["Image"] = image_url
                return results

def parseGuns(gun_string : str):
    """Receive gunString and return adequately parsed guns"""
    if "," not in gun_string:
        # Replace spaces with underscores
        gun_string = gun_string.replace(" ","_")
        return (gun_string, None)
    else:
        # Split into two variables, gun1 and gun2, taking into account comma habits.
        try:
            gun1, gun2 = gun_string.split(", ")
        except ValueError:
            gun1, gun2 = gun_string.split(",")
        # Replace spaces with underscores
        gun1 = gun1.replace(" ","_")
        gun2 = gun2.replace(" ","_")
        return gun1, gun2

class Girlsfrontline:
    """Various commands for the mobile game GIRLS' FRONTLINE."""

    def __init__(self, bot):
        self.bot = bot

    async def checkGunExists(self, gun_string : str, gun : str, gun_data : dict) -> bool:
        """Checks if the given gun was not found."""
        if gun_data is None:
            if "," not in gun_string and " " in gun_string:
                suggestion = " Perhaps you left out the comma?"
            else:
                suggestion = ""
            await self.bot.say("Unable to find **{}**. Please check your spelling.{}".format(gun, suggestion))
            return False
        else:
            return True

    @commands.command(pass_context=True, aliases=["comparegun", "comapareguns", "comapreguns", "comapregun"])
    async def compareguns(self, ctx, *, guns : str):
        """Compare or lookup the stats of various T-Dolls.
        Compare by doing `!k.compareguns gun1, gun2` and lookup by using `!k.compareguns gun`.
        Gun names are case sensitive, eg do `Welrod MkII` not `welrod mkii`."""
        # Parse the guns string
        gun1, gun2 = parseGuns(guns)
        # Get data (: dict) of first gun
        await self.bot.send_typing(ctx.message.channel)
        gun1_data = await getData(gun1)
        # Check for Error 404
        if not await self.checkGunExists(guns, gun1, gun1_data):
            return
        # Check if this is a lookup or a compare by checking if gun2 is type : None
        if gun2 is None:
            gun2_data = {
                "Health" : "0",
                "5xLinked Health" : "0",
                "Damage" : "0",
                "Evasion" : "0",
                "Accuracy" : "0",
                "RoF" : "0",
                "Move Speed" : "0",
                "Crit Rate" : "0",
                "Crit Damage" : "0"
            }
            title = "{}'s stats".format(gun1)
            desc = "Viewing max stats"
        else:
            gun2_data = await getData(gun2)
            if not await self.checkGunExists(guns, gun2, gun2_data):
                return
            title = "{}'s stats VS {}'s stats".format(gun1, gun2)
            desc = "Comparing max stats"
        # Create the Embed
        em = tools.createEmbed(title, desc)
        # Loop over the stats dict and add
        for stat in gun1_data:
            # Subtract only integer stats
            if stat not in ["Tile Buff", "Tile Grid", "Image"]:
                val = int(gun1_data[stat]) - int(gun2_data[stat])
                if val > 0 and gun2 is not None:
                    # If percentage
                    if stat in ["Crit Rate", "Crit Damage"]:
                        val = str(val) + "%"
                    # If positive value, bolden the number.
                    em.add_field(name=stat, value="**{}**".format(val))
                else:
                    # If percentage
                    if stat in ["Crit Rate", "Crit Damage"]:
                        val = "{}%".format(val)
                    em.add_field(name=stat, value=val)
            # If comparing tile buffs, add two fields, one for each gun's tile buffs
            elif stat == "Tile Buff":
                em.add_field(name="{}'s Tile Buff".format(gun1), value="\n".join(gun1_data[stat]))
                if gun2 is not None:
                    em.add_field(name="{}'s Tile Buff".format(gun2), value="\n".join(gun2_data[stat]))
            # If comparing tile grids, add two fields, one for each grid
            elif stat == "Tile Grid":
                # Create the 3x3 grid
                l = gun1_data[stat]
                grid = "\n".join(["".join(l[x:x + 3]) for x in range(0, 9, 3)])
                em.add_field(name="{}'s Tile Grid".format(gun1), value=grid)
                if gun2 is not None:
                    l = gun2_data[stat]
                    grid = "\n".join(["".join(l[x:x + 3]) for x in range(0, 9, 3)])
                    em.add_field(name="{}'s Tile Grid".format(gun2), value=grid)
            # If comparing images, add the image of the first T-Doll
            elif stat == "Image":
                em.set_footer(text=gun1, icon_url=gun1_data[stat])
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
