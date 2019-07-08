import asyncio, aiohttp, discord, math, os, random, shelve
from discord.ext import commands
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

try:
    import cPickle as pickle
except ImportError:
    import pickle

from cogs.utilities import checks, staticData, tools
from cogs.utilities.paths import Path

#constants
upload_folder = Path.upload_folder
TEMP_FOLDER = Path.temp_folder

def createExpeditionEmbed(data):
    title = "Expedition {}: {}".format(data["id"], data["name"])
    description = "Ships: **{}**".format(data["requirements"]["ships"])
    description += "\nDrums: **{}**".format(data["requirements"]["drums"])
    time_h, time_m = divmod(data["time"], 60)
    description += "\nTime: **{}:{:02.0f}**".format(time_h, time_m)
    em = tools.createEmbed(title=title, description=description)

    # level requirements
    value0 = "Flagship: **{}**\nTotal: **{}**".format(data["requirements"]["fs"], data["requirements"]["total"])
    em.add_field(name="Level Requirements", value=value0, inline=False)

    # hourly yields
    value1 = "Resources: {}".format(" / ".join(str(x) for x in data["yield"]["hourly"]))
    value1 += "\nHQ xp: {}\nShip xp: {}".format(data["exp"]["hourly"]["hq"], data["exp"]["hourly"]["ship"])
    em.add_field(name="Hourly Yield", value=value1, inline=False)

    # total yields
    value2 = "Resources: {}".format(" / ".join(str(x) for x in data["yield"]["total"]))
    value2 += "\nHQ xp: {}\nShip xp: {}".format(data["exp"]["total"]["hq"], data["exp"]["total"]["ship"])
    em.add_field(name="Total Yield", value=value2, inline=False)

    # rewards
    value3 = "Common: {}\nGreat Success: {}".format(data["reward"][0], data["reward"][1])
    em.add_field(name="Rewards", value=value3, inline=False)

    # great success rewards
    gs_hourly = " / ".join(str(int(y)) for y in [x*1.5 for x in data["yield"]["hourly"]])
    gs_total = " / ".join(str(int(y)) for y in [x*1.5 for x in data["yield"]["total"]])
    value4 = "Hourly: {}\nTotal: {}".format(gs_hourly, gs_total)
    em.add_field(name="Great Success Yields", value=value4, inline=False)

    return em

async def oaswSuggestions(bot, ctx, kanmusu):
    kanmusu = kanmusu.lower()
    if kanmusu == 'hibiki':
        suggestion = 'Verniy, Bep'
        await bot.send_message(ctx.message.channel, "Perhaps you meant _{}_".format(suggestion))

class Kancolle:
    """Commands related to Kantai Collection."""

    def __init__(self, bot):
        self.bot = bot
        #KC EVENT TIMER
        #self.event_countdown = bot.loop.create_task(self.calc_countdown())

    def __unload(self):
        #self.event_countdown.cancel()
        pass

    async def calc_countdown(self):
        await self.bot.wait_until_ready()
        FREQ = 60 # run task every minute
        message_id = "421155838439194633"
        event_channel = self.bot.get_channel("414474883360358410")
        countdown_message = await self.bot.get_message(channel=event_channel, id=message_id)
        TARGET_TIME = datetime(2018, 3, 23, 13)
        while not self.bot.is_closed:
            time_left = TARGET_TIME - datetime.now()
            d, s = time_left.days, time_left.seconds
            weeks, days = divmod(d, 7)
            m, seconds = divmod(s, 60)
            hours, minutes = divmod(m, 60)
            em = tools.createEmbed(title="Time Remaining", description="{} weeks, {} days, {} hours, {} minutes".format(weeks, days, hours, minutes))
            em.set_footer(text="Updates every {} second(s)".format(FREQ))
            await self.bot.edit_message(message=countdown_message, embed=em)
            await asyncio.sleep(FREQ)

    @commands.command()
    async def expedition(self, exped_number : str):
        """Lookup the data for a certain expedition."""
        with shelve.open("db\\expedition_db\\exped_db", "r") as shelf:
            try:
                data = shelf[exped_number]
            except KeyError:
                await self.bot.say("Could not find expedition `{}`".format(exped_number))
                return
        em = createExpeditionEmbed(data)
        await self.bot.say(embed=em)

    @commands.command(aliases=["jets"])
    async def jet(self, slot_size : int, nodes=1):
        """Lookup the steel consumption of jets based on slot size."""
        em = tools.createEmbed(title="Jet steel consumption costs", description="The amount of steel required per node for jet aircraft")
        jets = {
            "Kikka Kai" : 13,
            "Jet Keiun Kai" : 14
        }
        for jet in jets:
            em.add_field(name=jet, value=round(0.2 * jets[jet] * slot_size) * nodes)
        await self.bot.say(embed=em)

    @commands.command(aliases=["compareship", "comapareships", "comapareship", "comapreships", "comapreship"])
    async def compareships(self, *, args : str):
        """Compare the stats of two kanmusu with `!k.comapreships <ship1>, <ship2>`
        or lookup stats with `!k.compareships <ship>`"""
        ZERO_STAT_COMPARATOR = "0_stat"
        if ', ' not in args:
            firstShip = args
            secondShip = ZERO_STAT_COMPARATOR
        else:
            try:
                firstShip, secondShip = args.split(', ')
            except ValueError:
                await self.bot.say("`!k.compareships ship1, ship2` for stat comparison. `!k.compareships ship` for stat lookup.")
                return
        with shelve.open("db\\ship_db", "r") as shelf:
            try:
                ship1 = shelf[firstShip.lower()]
            except KeyError:
                await self.bot.say("Unable to find **{}**.".format(firstShip))
                if ', ' not in args:
                    await self.bot.say("Did you forget the comma? `!k.compareships ship1, ship2`")
                return
            try:
                ship2 = shelf[secondShip.lower()]
            except KeyError:
                await self.bot.say("Unable to find **{}**.".format(secondShip))
                if ', ' not in args:
                    await self.bot.say("Did you forget the comma? `!k.compareships ship1, ship2`")
                return
        if ship1 is None or ship2 is None:
            return
        else:
            #build the embed
            firstShipFormatted, secondShipFormatted = firstShip[0].upper() + firstShip[1:].lower(), secondShip[0].upper() + secondShip[1:].lower()
            if secondShip is not ZERO_STAT_COMPARATOR:
                title = "{}'s stats VS {}".format(firstShipFormatted, secondShipFormatted)
                description = "Comparing max stats (except luck)"
            else:
                title = "{}'s stats".format(firstShipFormatted)
                description = "{} stat lookup".format(firstShipFormatted)
            em = tools.createEmbed(title=title, description=description)
            em.set_image(url="https://github.com/Diablohu/WhoCallsTheFleet/blob/master/pics-ships-{}/{}/0.webp?raw=true".format(int(ship1['id'] / 50) + (0 if ship1['id'] % 50 == 0 else 1), ship1['id']))
            stats = [
                ('fire_max', 'Firepower'),
                ('torpedo_max', 'Torpedo'),
                ('aa_max', 'AA'),
                ('asw_max', 'ASW'),
                ('hp', 'HP'),
                ('armor_max', 'Armour'),
                ('evasion_max', 'Evasion'),
                ('luck', 'Luck'),
                ('fuel', 'Fuel Consumption'),
                ('ammo', 'Ammo Consumption'),
                ('base_lvl', 'Base Level'),
                ('slot', 'Plane Slots')
            ]
            for stat in stats:
                if ship1[stat[0]] == -1 or ship2[stat[0]] == -1:
                    statResult = 'No Data'
                elif stat[0] == "slot":
                    if secondShip != ZERO_STAT_COMPARATOR:
                        statResult = "{}: **{}**\n{}: **{}**".format(firstShipFormatted, ship1[stat[0]], secondShipFormatted, ship2[stat[0]])
                    else:
                        statResult = ship1[stat[0]]
                else:
                    statResult = ship1[stat[0]] - ship2[stat[0]]
                    if statResult > 0 and secondShip != ZERO_STAT_COMPARATOR:
                        statResult = "**+{}**".format(statResult)
                em.add_field(name=stat[1], value=statResult)
            await self.bot.say(embed=em)

    @commands.command(pass_context=True)
    async def gacha(self, ctx):
        """Test your luck in a virtual KC gacha!"""
        await self.bot.send_typing(ctx.message.channel)
        # BANNER SELECTION
        # Get banners. Standard banner dimensions = 760 x 100
        BANNER_WIDTH, BANNER_HEIGHT = 860, 100
        banners = [x for x in os.listdir(Path.gacha_folder) if x[-4:] == ".png" or x[-4:] == ".jpg"]
        banner_frame = Image.new("RGBA", (BANNER_WIDTH, BANNER_HEIGHT * len(banners)), (255, 0, 0, 0))
        banner_draw = ImageDraw.Draw(banner_frame)
        banner_font = ImageFont.truetype(r"C:\Windows\Fonts\Arial.ttf", 96)
        # Create banner list
        for banner in banners:
            # Load banner image and resize if needed
            banner_img = Image.open(Path.gacha_folder + "\\" + banner)
            if banner_img.size != (BANNER_WIDTH, BANNER_HEIGHT):
                banner_img.resize((BANNER_WIDTH, BANNER_HEIGHT))
            # Draw text and image onto frame
            index = banners.index(banner)
            banner_draw.text((0, index * 100), str(index + 1) + ".", (200, 200, 200), font=banner_font)
            banner_frame.paste(banner_img, (100, index * 100))
        # Save and output banner selection
        banner_f_name = Path.temp_folder + "\\" + "banner" + datetime.now().strftime("%Y-%m-%d %H-%M-%S") + ".png"
        banner_frame.save(banner_f_name)
        await self.bot.say("Please select a banner:")
        await self.bot.send_typing(ctx.message.channel)
        await self.bot.upload(banner_f_name)
        selection = await self.bot.wait_for_message(timeout=300, author=ctx.message.author, check=lambda x: checks.convertsToInt(x.content) and int(x.content) in range(1, len(banners) + 1))
        chosen_banner = banners[int(selection.content) - 1].split(".")[0] + ".pickle"

        msg = await self.bot.say("Fetching gacha results...")
        await self.bot.send_typing(ctx.message.channel)
        file_name = datetime.now().strftime("%Y-%m-%d %H-%M-%S") + ".png"
        # Load gacha statistics and calculate pull result
        gacha_data = tools.loadPickle(Path.gacha_folder + "\\{}".format(chosen_banner))
        pulls = random.choices(gacha_data["ship"], weights=gacha_data["count"], k=10)

        # Setup Pillow items
        # each icon 240 x 60
        frame_x, frame_y = 700, 600
        frame = Image.new("RGBA", (frame_x, frame_y), (255, 0, 0, 0))
        draw = ImageDraw.Draw(frame)
        font = ImageFont.truetype(r"C:\Windows\Fonts\Arial.ttf", 48)
        
        # Add each pull and its text to the frame
        count = 0 # Cannot use index due to duplicates
        for pull in pulls:
            # Attempt to load image from cache
            try:
                cg = Image.open(Path.gacha_cache + "\\{}0.png".format(pull))
            except FileNotFoundError:
                # Not in cache, attempt to load from web url
                try:
                    with shelve.open("db\\ship_db", "r") as shelf:
                        ship_id = shelf[pull.lower()]["id"]
                except KeyError:
                    await self.bot.say("Could not find **{}**. Please check your spelling.".format(pull))
                    return
                url = "https://github.com/Diablohu/WhoCallsTheFleet/blob/master/pics-ships-{}/{}/0.webp?raw=true".format(int(ship_id / 50) + (0 if ship_id % 50 == 0 else 1), ship_id)
                async with aiohttp.get(url) as response:
                    if response.status != 404:
                        cg = Image.open(BytesIO(await response.read()))
                        # Save CG to cache
                        cg.save(Path.gacha_cache + "\\{}0.png".format(pull))
                    else:
                        await self.bot.say("Could not find a CG for **{}**.".format(pull))
                        return

            # Add CG and Name text
            frame.paste(cg, (0, count * 60))
            draw.text((260, count * 60), pull.upper(), (200, 200, 200), font=font)
            count += 1
        
        # Save, output and delete files from tmp
        result = Path.temp_folder + "\\" + file_name
        frame.save(result)
        await self.bot.delete_message(msg)
        await self.bot.upload(result)
        tools.clearTempFolder()

    @commands.command(pass_context=True, hidden=True)
    async def boat(self, ctx, *, ship_name : str):
        """Display a kanmusu info card."""
        file_name = datetime.now().strftime("%Y-%m-%d %H-%M-%S") + ".png"
        SPECIAL_CASES = {
            "commandant": "teste",
            "ark": "royal",
            "prinz": "eugen",
            "graf": "zeppelin",
            "giuseppe": "garibaldi"
        }
        kanmusu = ship_name.lower()
        await self.bot.send_typing(ctx.message.channel)

        try:
            with shelve.open("db\\ship_db", "r") as shelf:
                ship_id = shelf[kanmusu]["id"]
        except KeyError:
            await self.bot.say("I couldn't find **{}**.".format(kanmusu))
            return

        url = "https://github.com/Diablohu/WhoCallsTheFleet/blob/master/pics-ships-{}/{}/8.webp?raw=true".format(int(ship_id / 50) + (0 if ship_id % 50 == 0 else 1), ship_id)
        async with aiohttp.get(url) as response:
            if response.status != 404:
                # Get the shipgirl's CG
                cg = Image.open(BytesIO(await response.read()))
            else:
                # Couldn't find CG
                kanmusu = ship_name.lower().split(" ")[0] # Strip any potential tags (accounts for no CG change on kai etc)
                # SPECIAL CASE CATCH
                if kanmusu in SPECIAL_CASES:
                    kanmusu = "{} {}".format(kanmusu, SPECIAL_CASES[kanmusu])
                try:
                    with shelve.open("db\\ship_db", "r") as shelf:
                        ship_id = shelf[kanmusu]["id"]
                except KeyError:
                    await self.bot.say("I couldn't find **{}**.".format(kanmusu))
                    return

                # Try to retrieve CG again
                url = "https://github.com/Diablohu/WhoCallsTheFleet/blob/master/pics-ships-{}/{}/8.webp?raw=true".format(int(ship_id / 50) + (0 if ship_id % 50 == 0 else 1), ship_id)
                async with aiohttp.get(url) as response:
                    if response.status == 404:
                        # Still couldn't find CG, return.
                        return
                    else:
                        cg = Image.open(BytesIO(await response.read()))

            # Save CG as PNG
            cg.save(TEMP_FOLDER + "\\cg.png") # Store in tmp folder
            base_template = Image.open(upload_folder + "\\base_style_template.png")
            draw = ImageDraw.Draw(base_template)
            font = ImageFont.truetype(r"C:\Windows\Fonts\Arial.ttf", 48) # (font, font_size)
            template_x, template_y = base_template.size
            cg_x, cg_y = cg.size

            # Draw text and paste images onto template
            draw.text((150, 95), ship_name.upper(), (150, 150, 150), font=font)
            base_template.paste(cg, (template_x - cg_x, 0), cg)
            
            # Save result to tmp
            result = TEMP_FOLDER + "\\" + file_name
            base_template.save(result)
            
            # Output image
            await self.bot.upload(result)

            # Clear tmp
            tools.clearTempFolder()

    @commands.group(pass_context=True)
    async def lbas(self, ctx):
        """Display LBAS aircraft information."""
        if ctx.invoked_subcommand is None:
            await tools.uploadImage(self.bot, ctx, filename="lbas")

    @lbas.command(pass_context=True)
    async def range(self, ctx, lowest_range=None):
        """Display the LBAS range bonuses given by various recon aircraft."""
        if lowest_range is None:
            await tools.uploadImage(self.bot, ctx, filename="lbas_range")
        else:
            try:
                data = staticData.lbasRangeData(lowest_range)
                output = "LBAS range bonusses:\n" + "\n".join(["{}:\n{:>4}\n".format(x, data[x]) for x in data])
                await self.bot.say("```{}```".format(output))
            except IndexError:
                await self.bot.say("Please enter a range between 2 and 9")

    @commands.command(pass_context=True, aliases=["tci_rates"])
    async def tci(self, ctx):
        """View a table showing torpedo cut in luck rates."""
        await tools.uploadImage(self.bot, ctx, filename="tci")

    @commands.command(pass_context=True, aliases=["overkill_rates"])
    async def overkill(self, ctx):
        """View overkill rates based on HP."""
        await tools.uploadImage(self.bot, ctx, filename="overkill_rates")

    @commands.command(pass_context=True, aliases=["tank", "tankhatsu"])
    async def tanks(self, ctx):
        """Display who can carry what daihatsus."""
        await tools.uploadImage(self.bot, ctx, filename="daihatsu_carriers")

    @commands.command(pass_context=True, aliases=["daihatsu"])
    async def toku(self, ctx):
        """Display Expedition bonuses from daihatsu landing crafts"""
        await tools.uploadImage(self.bot, ctx, filename="toku")

    @commands.command(pass_context=True)
    async def cvci(self, ctx):
        """Display information for aircraft carrier day cut in."""
        await tools.uploadImage(self.bot, ctx, filename="cvci")

    @commands.command(pass_context=True)
    async def damage(self, ctx):
        """Display the main damage formula."""
        await tools.uploadImage(self.bot, ctx, filename="damage")
    
    @commands.command(pass_context=True, aliases=["basic", "attack", "attack_power", "atk_power", "damage2"])
    async def basicatk(self, ctx):
        """Display the basic attack power formulas."""
        await tools.uploadImage(self.bot, ctx, filename="damage2")

    @commands.command(pass_context=True)
    async def defense(self, ctx):
        """Display the formula for defense power."""
        await tools.uploadImage(self.bot, ctx, filename="defense")

    @commands.command(pass_context=True)
    async def scratch(self, ctx):
        """Display the scratch damage formula."""
        await tools.uploadImage(self.bot, ctx, filename="scratch")

    @commands.command(pass_context=True)
    async def vanguard(self, ctx):
        """Display the modifiers for Vanguard (spoon) formation."""
        await tools.uploadImage(self.bot, ctx, filename="vanguard")

    @commands.command(pass_context=True)
    async def yasen(self, ctx):
        """Display the equipment setups for special night battle attacks."""
        await tools.uploadImage(self.bot, ctx, filename="yasen")

    @commands.command(pass_context=True, aliases=["carrier_yasen", "cv_yasen", "yasen_cvci", "cvci_yasen", "cvci2"])
    async def yasen2(self, ctx):
        """Display the equipment setups required for carrier night battle attacks."""
        await tools.uploadImage(self.bot, ctx, filename="yasen2")

    @commands.command(pass_context=True)
    async def aaci(self, ctx):
        """Display an AACI info chart."""
        await tools.uploadImage(self.bot, ctx, filename="aaci")

    @commands.command(pass_context=True, aliases=["recipes", "development"])
    async def recipe(self, ctx):
        """View the quick equip recipe guide."""
        await tools.uploadImage(self.bot, ctx, filename="recipe")

    @commands.command(pass_context=True)
    async def classes(self, ctx):
        """View destroyer gun and torpedo class categories."""
        await tools.uploadImage(self.bot, ctx, filename="destroyer_class_bonuses")

    @commands.command(pass_context=True)
    async def fit(self, ctx):
        """Displays overweight penalties and fit guns for battleships."""
        await tools.uploadImage(self.bot, ctx, filename="fit")

    @commands.command(pass_context=True)
    async def fit2(self, ctx):
        """Display fit bonuses for cruisers."""
        await tools.uploadImage(self.bot, ctx, filename="fit2")

    @commands.command(pass_context=True, aliases=["dgun", "cgun", "destroyerfit", "ddfit", "kagerou", "naganami"])
    async def fit3(self, ctx):
        """Display fit bonuses for destroyers."""
        await tools.uploadImage(self.bot, ctx, filename="fit3")
        #await self.bot.say("https://i.imgur.com/dxy5NQi.png")
        await tools.uploadImage(self.bot, ctx, filename="bonus_small_guns")

    @commands.command(pass_context=True)
    async def greatsuccess(self, ctx):
        """Display great success chances for expeditions."""
        await tools.uploadImage(self.bot, ctx, filename="greatsuccess")
    
    @commands.command(pass_context=True, aliases=["shuzii"])
    async def luck(self, ctx, ship_luck="", ship_level=""):
        """Display the night cut-in formula or calculate your chance of cutting in by providing the luck value of your ship."""
        if ship_luck == "" and ship_level == "":
            # Display the night cut in formula
            await tools.uploadImage(self.bot, ctx, filename="luck")
        elif checks.convertsToInt([ship_luck, ship_level]) and int(ship_luck) > 0 and int(ship_level) > 0: # Check positive and non-zero integer parameters
            # Convert params to int
            ship_luck, ship_level = int(ship_luck), int(ship_level)
            # Create cut in type embed prompt and get type value
            cut_ins = ["Gun Cut-in", "Mixed Gun Cut-in", "Torpedo Cut-in", "Mixed Torpedo Cut-in"]
            type_factors = {
                1 : 140,
                2 : 130,
                3 : 122,
                4 : 115
            }
            description = ""
            for x in cut_ins:
                description += "**{}.** {}\n".format(cut_ins.index(x) + 1, x)
            em = tools.createEmbed(title="Select your night cut-in setup:", description=description)
            question = await self.bot.say(embed=em)
            response = await self.bot.wait_for_message(timeout=300, author=ctx.message.author, check=lambda x: checks.convertsToInt(x.content) and int(x.content) in range(1, 5))
            if response is None:
                return
            elif checks.convertsToInt(response.content) and int(response.content) in range(1, 5):
                type_factor = type_factors[int(response.content)]
                await self.bot.delete_messages([question, response])
            
            # Create modifier embed prompt and get modifier values
            modifiers = ["Is flagship", "Is chuuha", "Searchlight active", "Star shell active", "Has skilled lookout"]
            modifier_values = {
                1 : 15,
                2 : 18,
                3 : 7,
                4 : 4,
                5 : 5
            }
            description = "example input: `1, 2, 5`\n\n"
            for x in modifiers:
                description += "**{}.** {}\n".format(modifiers.index(x) + 1, x)
            description += "\n**0.** NONE"
            emb = tools.createEmbed(title="Select applicable modifiers:", description=description)
            question = await self.bot.say(embed=emb)
            response = await self.bot.wait_for_message(timeout=300, author=ctx.message.author, check=lambda x: checks.convertsToInt(x.content.replace(" ","").split(",")) and all([0 <= int(y) <= len(modifiers) for y in x.content.replace(" ","").split(",")]))
            if response is None:
                return
            elif response.content == "0":
                selections = []
                modifier = 0
                await self.bot.delete_messages([question, response])
            elif checks.convertsToInt(response.content.replace(" ","").split(",")) and all([1 <= int(x) <= len(modifiers) for x in response.content.replace(" ","").split(",")]):
                # parse the response and obtain total modifier value
                selections = [int(x) for x in response.content.replace(" ","").split(",")]
                modifier = sum([modifier_values[x] for x in selections])
                await self.bot.delete_messages([question, response])
            
            # Calculate Cut-in chance
            if ship_luck < 50:
                base_value = int(15 + ship_luck + 0.75 * math.sqrt(ship_level) + modifier)
            else:
                base_value = int(65 + math.sqrt(ship_luck - 50) + 0.8 * math.sqrt(ship_level) + modifier)
            cutin_chance = base_value / type_factor
            description = "Luck: {}\nLevel: {}\n".format(ship_luck, ship_level)
            if selections != []:
                description += "Modifiers: {}".format(", ".join([modifiers[x-1] for x in selections]))
            await self.bot.say(embed=tools.createEmbed(title="Cut-in Chance: {:.2%}".format(cutin_chance), description=description))

        else:
            await self.bot.say("Are you missing some parameters?")


    @commands.command(pass_context=True)
    async def oasw(self, ctx):
        """Link to wikia OASW tables."""
        '''
        #async def oasw(self, ctx, *, kanmusu : str):
        oasw_database = tools.loadPickle('oasw_database.pickle')
        kanmusu = kanmusu.split(' ')[0].lower() # strip off any unnecessary tags (such as 'kai', 'kai ni', etc.)
        try:
            data = oasw_database[kanmusu]
        except KeyError:
            await self.bot.say("Unable to find **{}'s** data. Remember to use long sounds eg. _Y**uu**dachi_, not _Y**u**dachi_.".format(kanmusu[0].upper() + kanmusu[1:]))
            await oaswSuggestions(self.bot, ctx, kanmusu)
            return
        tags = oasw_database[len(oasw_database[kanmusu])]
        title = "{}'s Opening ASW data".format(kanmusu[0].upper() + kanmusu[1:])
        description = "Assuming highest kai'd form..."
        em = tools.createEmbed(title=title, description=description)
        for x in tags:
            em.add_field(name=x, value=data[tags.index(x)])
        await self.bot.say(embed=em)
        '''
        await self.bot.say("http://kancolle.wikia.com/wiki/Oasw")

    @commands.command()
    async def akashi(self):
        """Akashi's arsenal information (link to akashi-list)."""
        await self.bot.say('http://akashi-list.me')

    @commands.command()
    async def world(self, level : str):
        """View information for a specified map X-X."""
        if len(level) != 3 or level[1] != '-':
            await self.bot.say("Please do '!k.world N-N', where N is the world level.")
        else:
            field = (level[0], level[2])
            file_origin = Path.world_info
            await self.bot.say("World {}-{} Map and branching rules:".format(field[0], field[1]))
            try:
                await self.bot.upload(file_origin + '\\{0}-{1}_Map.jpg'.format(field[0], field[1]))
            except Exception:
                try:
                    await self.bot.upload(file_origin + '\\{0}-{1}_Map.png'.format(field[0], field[1]))
                except Exception as e:
                    await self.bot.say("Unable to retrieve World {0}-{1} map info.".format(field[0], field[1]))
                    #await self.bot.say('{}: {}'.format(type(e).__name__, e))
            try:
                await self.bot.upload(file_origin + '\\{0}-{1}.png'.format(field[0], field[1]))
            except Exception:
                try:
                    await self.bot.upload(file_origin + '\\{0}-{1}.jpg'.format(field[0], field[1]))
                except Exception as e:
                    await self.bot.say("Unable to retrieve World {0}-{1} branching rules info.".format(field[0], field[1]))
                    #await self.bot.say('{}: {}'.format(type(e).__name__, e))
            try:
                nodes = staticData.airPower(int(field[0]), int(field[1]))
                data = 'Node/AS/AS+\n\n'
                for x in nodes:
                    data += "{0} - **{1}**, {2}\n".format(x, nodes[x][0], nodes[x][1])
                title = "{}-{} Air Superiority Requirements".format(field[0], field[1])
                em = tools.createEmbed(title=title, description=data)
                await self.bot.say(embed=em)
                #await self.bot.say('```Air superiority requirements\n{}```'.format(data))
            except Exception as e:
                await self.bot.say("Unable to display AS data.")
                #await self.bot.say('{}: {}'.format(type(e).__name__, e))
            #Provide wikia link
            await self.bot.say("Wikia world page: <http://kancolle.wikia.com/wiki/World_{0}#/{0}-{1}>".format(field[0], field[1]))

    '''
    @commands.command(pass_context=True)
    async def update(self, ctx, *, current_status : str):
        """Update the Kancolle Event Status Board with your current status.
        eg. `!k.update Clearing E5H`
        Only available on Hourai private server."""
        if not checks.check_hourai(ctx.message):
            return
        else:
            # Retrieve Kamikaze's message data
            message_id = "414614925978238988"
            event_channel = self.bot.get_channel("414474883360358410")
            status_message = await self.bot.get_message(channel=event_channel, id=message_id)

            # save current embed info
            em = status_message.embeds[0]
            new_em = tools.createEmbed(title="Event Status", description="What Admirals are currently doing in the event.\nUpdate yours with `!k.update <message>`.")
            try:
                users = [em["fields"][x]["name"] for x in range(len(em["fields"]))]
                user_values = [em["fields"][x]["value"] for x in range(len(em["fields"]))]
                data_exists = True
            except KeyError:
                data_exists = False

            if data_exists:
                if ctx.message.author.name in users:
                    # pop them if they're already on the list
                    kill_index = users.index(ctx.message.author.name)
                    users.pop(kill_index)
                    user_values.pop(kill_index)
            new_em.add_field(name=ctx.message.author.name, value=current_status)
            # recreate the embed using old embed data
            if data_exists:
                for user in users:
                    new_em.add_field(name=user, value=user_values[users.index(user)])
            # edit the message
            await self.bot.edit_message(message=status_message, embed=new_em)
            await self.bot.say("Updated your current event status!")
    '''

    '''
    @commands.command(pass_context=True)
    async def medals(self, ctx, *, map_difficulties : str):
        """Update the Kancolle Event Medal Tally with your current clears.
        eg. `!k.medals HHCEMHH`
        Use `!k.medals x` to clear your medal list.
        Only available on Hourai private server."""
        if not checks.check_hourai(ctx.message):
            return
        else:
            event_length = 7
            message_id = "414827581624549386"
            event_channel = self.bot.get_channel("414474883360358410")
            medal_message = await self.bot.get_message(channel=event_channel, id=message_id)

            # save current embed info
            em = medal_message.embeds[0]
            new_em = tools.createEmbed(title="Difficulty Clear Status", description="Event medals that Admirals have currently obtained.\nUpdate yours with `!k.medals <medal string/eg.HHHMME>`\nYou can clear with `!k.medals x`.")
            try:
                users = [em["fields"][x]["name"] for x in range(len(em["fields"]))]
                user_values = [em["fields"][x]["value"] for x in range(len(em["fields"]))]
                data_exists = True
            except KeyError:
                data_exists = False

            # dictionary translations
            parse = {
                "C" : "<:EventMedalCasual:414828756130070529>",
                "E" : "<:EventMedalEasy:414829530910425108>",
                "M" : "<:EventMedalNormal:414829531283849227>",
                "N" : "<:EventMedalNormal:414829531283849227>",
                "H" : "<:EventMedalHard:414829531334180884>",
                "X" : ":no_entry_sign:"
            }

            # parse difficulty string
            map_difficulties = map_difficulties.upper().replace(' ','').replace(',','')
            if len(map_difficulties) > event_length:
                await self.bot.say("That's more than 7 medals there. Please look it over and try again.")
                return
            parsed_str = ""
            for x in map_difficulties:
                if x not in ['C','E','M','N','H','X']:
                    await self.bot.say("Hmmm, I can't translate that to medals. Try `C`, `E`, `M/N`, and `H`.")
                    return
                parsed_str += parse[x]

            if data_exists:
                if ctx.message.author.name in users:
                    # pop them if they're already on the list
                    kill_index = users.index(ctx.message.author.name)
                    users.pop(kill_index)
                    user_values.pop(kill_index)
            new_em.add_field(name=ctx.message.author.name, value=parsed_str)
            # recreate the embed using old embed data
            if data_exists:
                for user in users:
                    new_em.add_field(name=user, value=user_values[users.index(user)])
            # edit the message
            await self.bot.edit_message(message=medal_message, embed=new_em)
            await self.bot.say("Updated your event medal tally!")
    '''

def setup(bot):
    bot.add_cog(Kancolle(bot))
