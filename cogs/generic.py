import discord, asyncio, random, os
from discord.ext import commands
from cogs.utilities import paths, tools, checks
from datetime import datetime, timedelta

#constants
UPLOAD_FOLDER = paths.uploadFolder()
UNLISTED_COGS = ['Loader', 'Repl', 'Keywords']

def removeMicroseconds(tdelta):
    return tdelta - timedelta(microseconds=tdelta.microseconds)

class Generic:
    """A range of general and misc functionality commands."""

    def __init__(self, bot):
        self.bot = bot

    def createCogHelpEmbed(self):
        """Create the help output that lists all of Kamikaze's cogs."""
        title = "HELP - List of categories"
        description = "A list of Kamikaze's command categories. Use `!k.help <category>` for more help."
        em = tools.createEmbed(title=title, description=description)
        for cog in self.bot.cogs:
            if cog not in UNLISTED_COGS:
                em.add_field(name=cog, value=self.bot.cogs[cog].__doc__, inline=False)
        return em

    def displayFinalHelpCommand(self, cmd):
        """Create and return the help embed for a command with no sub commands."""
        params = ['<'+x+'>' for x in cmd.params if x not in ['self', 'ctx']]
        title = "HELP - '{}'".format(cmd)
        description = "**{}**\n\n__Usage__\n`!k.{} {}`".format(cmd.help, cmd, ' '.join(params))
        return tools.createEmbed(title=title, description=description)

    def processHelpCommand(self, cmd):
        """Parse the keyword and display appropriately formatted command help."""
        #return tools.createEmbed(title="WIP", description="Command help not yet implemented") # STUB
        all_commands = [x for x in self.bot.walk_commands()]
        # check if the command has sub commands
        sub_commands = []
        for command in all_commands:
            if str(command).startswith(str(cmd) + ' '):
                sub_commands.append(command)
        if len(sub_commands) > 0: # then the command has sub commands
            title = "HELP - '{}'".format(cmd)
            description = "**{}**\n\nThe following is a list of subcommands under the **{} command**.\nUse `!k.help {} <subcommand>` for more detailed help.".format(cmd.help, cmd, cmd)
            em = tools.createEmbed(title=title, description=description)
            for command in sub_commands:
                em.add_field(name=command.name, value=command.help, inline=False)
            return em
        else: # the command doesn't have any sub commands
            return self.displayFinalHelpCommand(cmd)

    def processHelpKeyword(self, keyword):
        """Parse the keyword and display the appropriate help page."""
        cmd = self.bot.get_command(keyword.lower())
        # first check if the keyword is a cog:
        casedKeyword = keyword[0].upper() + keyword[1:].lower()
        if casedKeyword in self.bot.cogs and casedKeyword not in UNLISTED_COGS:
            title = "HELP - '{}' commands".format(casedKeyword)
            description = "List of commands under the **{} category**. Use `!k.help <command>` for more detail.".format(casedKeyword)
            em = tools.createEmbed(title=title, description=description)
            # add the cog's commands to its help page
            for command in self.bot.commands:
                commandObj = self.bot.get_command(command)
                if keyword.lower() == commandObj.module.__name__.replace('cogs.','') and not commandObj.hidden: #splice off "cogs."
                    em.add_field(name=command, value=commandObj.help, inline=False)
            return em
        # else, check if the keyword is a command/subcommand:
        #elif keyword.lower() in [x.lower() for x in self.bot.commands]:
        elif cmd is not None:
            return self.processHelpCommand(cmd)
        # else, output an error message
        else:
            description = "What you entered is neither a category nor command. Please check your case/spelling and try again."
            em = tools.createEmbed(title="HELP - '{}'".format(keyword), description=description)
            return em

    @commands.command(pass_context=True)
    async def test(self, ctx):
        await self.bot.say(ctx.message.channel.name is None)

    @commands.command(pass_context=True)
    async def help(self, ctx, *, keyword=""):
        """Show this help command. Lookup various categories and commands with this."""
        destination = ctx.message.author
        #if raw !k.help, show available cogs
        if keyword == "":
            await self.bot.send_message(destination, embed=self.createCogHelpEmbed())
        else:
            await self.bot.send_message(destination, embed=self.processHelpKeyword(keyword))

    @commands.group(pass_context=True)
    async def countdown(self, ctx):
        """Displays the remaining time until a specified event."""
        # Check if the server is already in the list, if not, add a dummy datetime
        countdown_all = tools.loadPickle('countdown_all.pickle')
        try:
            countdown_server = countdown_all[ctx.message.server.id]
        except KeyError:
            countdown_all[ctx.message.server.id] = [datetime.now(), "remain"]
            tools.dumpPickle(countdown_all, 'countdown_all.pickle')
            countdown_server = countdown_all[ctx.message.server.id]

        if ctx.invoked_subcommand is None:
            if countdown_server[0] > datetime.now():
                tdelta = countdown_server[0] - datetime.now()
                text = countdown_server[1]
            else:
                tdelta = datetime(year=2100, month=10, day=10, hour=10, minute=10, second=10) - datetime.now()
                text = "until nothing happens..."
            #await self.bot.say("`{}` {}".format(removeMicroseconds(tdelta), text))
            #await self.bot.say(embed=tools.createEmbed(title="{} {}".format(removeMicroseconds(tdelta), text)))
            await self.bot.say(embed=tools.createEmbed(title=str(removeMicroseconds(tdelta)), description=text))

    @countdown.command(pass_context=True)
    async def edit(self, ctx):
        """Edit the countdown target."""
        AUTO_TIMEOUT = 300 # 5 minutes
        if checks.check_moderator(ctx.message):
            info1 = await self.bot.say("Please enter a new target date in format: **DD-MM-YYYY, HH:MM:SS**")
            msg1 = await self.bot.wait_for_message(timeout=AUTO_TIMEOUT, author=ctx.message.author)
            if msg1 is None:
                await tools.inputTimeout(self.bot, ctx, topic="countdown edit")
                return
            else:
                try:
                    newTime = datetime.strptime(msg1.content, '%d-%m-%Y, %H:%M:%S')
                except ValueError:
                    await self.bot.say("Sorry, formatting was incorrect. Remember to include 0s where needed. Try _!k.countdown edit_ again.")
                    return
            info2 = await self.bot.say("Please enter the countdown timer's flavour text:")
            msg2 = await self.bot.wait_for_message(timeout=AUTO_TIMEOUT, author=ctx.message.author)
            if msg2 is None:
                await tools.inputTimeout(self.bot, ctx, topic="countdown edit")
                return
            else:
                text = msg2.content
                countdown_all = tools.loadPickle('countdown_all.pickle')
                countdown_all[ctx.message.server.id] = [newTime, text]
                tools.dumpPickle(countdown_all, 'countdown_all.pickle')
                await self.bot.delete_messages([info1, msg1, info2, msg2])
                await self.bot.say("Successfully updated the server countdown target!")
        else:
            await self.bot.say("You do not have permission to do that.")
            return

    @commands.command(pass_context=True)
    async def count(self, ctx, *, count_what : str):
        """Get Kamikaze to count something for you. 1 transport, 2 transports..."""
        AUTO_TIMEOUT = 10800 # 3 hours
        count = 0
        title = "{}'s counter".format(ctx.message.author.name)
        description = "Increment count with _count N_, _cancel_ to stop."
        em = tools.createEmbed(title=title, description=description)
        em.add_field(name=count_what, value=count)
        info = await self.bot.say(embed=em)
        msg = await self.bot.wait_for_message(timeout=AUTO_TIMEOUT, author=ctx.message.author, check=lambda x: x.content.split(' ')[0].lower() in ['count', 'cancel'])
        try:
            while msg.content.lower() != 'cancel':
                try:
                    count += int(msg.content.strip('count '))
                    em.set_field_at(index=0, name=count_what, value=count)
                    await self.bot.delete_messages([info, msg])
                    info = await self.bot.say(embed=em)
                    msg = await self.bot.wait_for_message(timeout=AUTO_TIMEOUT, author=ctx.message.author, check=lambda x: x.content.split(' ')[0].lower() in ['count', 'cancel'])
                except ValueError:
                    await self.bot.say("Syntax should _count N_ where N is the number to increment by.")
        except AttributeError:
            await self.bot.say("{} your count for _{}_ has timed out. Last count: **{}**".format(ctx.message.author.mention, count_what, count))
            return
        await self.bot.say("Stopped counting.")

    @commands.command(pass_context=True)
    async def avatar(self, ctx, *, user : str):
        """View a user's profile picture. (!k.avatar @user)"""
        user_id = user.strip('<@>')
        member = ctx.message.server.get_member(user_id)
        title = "{}'s avatar".format(member.name)
        em = tools.createEmbed(title=title)
        em.set_image(url=member.avatar_url)
        await self.bot.say(embed=em)

    @commands.command(pass_context=True)
    async def notepad(self, ctx, *, content : str=None):
        """Store some text for later viewing. Clear with '!k.notepad clear.'"""
        data = tools.loadPickle('notepad.pickle')
        author = ctx.message.author
        if content is None:
            try:
                title = "{}'s Notepad".format(author.name)
                description = ''
                for x in data[author.id]:
                    description += "{}\n".format(x)
                em = discord.Embed(title=title, description=description, colour=author.colour)
                await self.bot.say(embed=em)
            except KeyError:
                await self.bot.say("You haven't written anything in your notepad... (￣～￣;)")
        elif content == 'clear':
            data[author.id] = []
            tools.dumpPickle(data, 'notepad.pickle')
            await self.bot.say('Your notepad has been cleared~ ( ^ _ ^ )')
        else:
            try:
                data[author.id].append(content)
                tools.dumpPickle(data, 'notepad.pickle')
                await self.bot.say("Successfully saved to your notepad! ＼(￣▽￣)／")
            except KeyError: # when it is first time data appending:
                await self.bot.say('Setting up your notepad for the first time~ ( ´ ▽ ` )')
                data[author.id] = []
                data[author.id].append(content)
                tools.dumpPickle(data, 'notepad.pickle')
                await self.bot.say("Successfully saved to your notepad! ＼(￣▽￣)／")

    @commands.command()
    async def fact(self):
        """Kamikaze shares her 90+ years of knowledge."""
        with open('fact_database', 'r') as f:
            chosen_fact = str(random.choice(f.readlines()))
        await self.bot.say('```{}```'.format(chosen_fact))

    @commands.command()
    async def up(self, item : str):
        """Display one of Kamikaze's many images."""
        if '\\' in item:
            pass
        elif item == 'list':
            item_list = []
            for x in os.listdir(UPLOAD_FOLDER):
                item_list.append(str(x).strip('[]'))
            await self.bot.say('```{}```'.format(item_list))
        elif item in os.listdir(UPLOAD_FOLDER): # make certain to keep kamikaze_bot.py in her directory, and that the file dir is correct
            await self.bot.upload(UPLOAD_FOLDER + '\\' + item)
        else:
            try:
                await self.bot.upload(UPLOAD_FOLDER + '\\{}.jpg'.format(item))
            except Exception:
                try:
                    await self.bot.upload(UPLOAD_FOLDER + '\\{}.png'.format(item))
                except Exception:
                    pass

    @commands.command()
    async def ping(self):
        """Ping Kamikaze."""
        await self.bot.say("Pong!")

    @commands.command(pass_context=True)
    async def server_info(self, ctx):
        """Find out about the server and its administrators."""
        try:
            server = ctx.message.server
            description = "**Server owner:** {}#{}\n".format(server.owner.name, server.owner.discriminator)
            description += "**Server region:** {}\n".format(server.region)
            adminList = []
            for member in server.members:
                if ctx.message.channel.permissions_for(member).administrator:
                    adminList.append(member.name)
            description += "\n**Administrators:**\n" + ', '.join(adminList)
            title = "Server Information: {}".format(server.name)
            em = tools.createEmbed(title=title, description=description)
            await self.bot.say(embed=em)
        except Exception as e:
            await self.bot.say("{}: {}".format(type(e).__name__, e))

    @commands.command()
    async def info(self):
        """Display info about Kamikaze."""
        owner = await self.bot.get_user_info("178112312845139969")
        title = "Information about Kamikaze"
        description = "I am a Discord bot written in python using Rapptz's discord api wrapper.\n"
        description += "I was written by **{}**.\n".format(owner)
        description += "My sourcecode can be found here: https://github.com/nath1100/Kamikaze-Bot"
        em = tools.createEmbed(title=title, description=description)
        # dependencies
        depends = "**Rapptz's API wrapper:** https://github.com/Rapptz/discord.py\n"
        depends += "Version {}".format(discord.__version__)
        em.add_field(name="Dependencies", value=depends, inline=False)
        # other credits
        credits = "**Diablohu's KC data:** https://github.com/Diablohu/WhoCallsTheFleet/"
        em.add_field(name="Other credits", value=credits, inline=False)
        await self.bot.say(embed=em)

    @commands.command()
    async def github(self):
        """Get Kamikaze's github repository."""
        await self.bot.say("You can find my sourcecode here: https://github.com/nath1100/Kamikaze-Bot")

def setup(bot):
    bot.add_cog(Generic(bot))
