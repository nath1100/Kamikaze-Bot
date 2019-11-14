import discord, os, asyncio, datetime
from discord.ext import commands
from cogs.utilities import checks, tools
try:
    import cPickle as pickle
except ImportError:
    import pickle

class Admin:
    """Various commands for Administrators."""

    def __init__(self, bot):
        self.bot = bot
        self.silenced = []

    @commands.command(pass_context=True, hidden=True)
    async def get_discord_version(self, ctx):
        """Output the discord.py version."""
        if checks.check_owner(ctx.message):
            await self.bot.say("discord.py version: **{}**".format(discord.__version__))

    @commands.command(pass_context=True, hidden=True)
    async def return_id_info(self, ctx, target_id : str):
        """Lookup an ID."""
        if checks.check_owner(ctx.message):
            server = self.bot.get_server(id=target_id)
            if server is None:
                for x in self.bot.servers:
                    if x.get_member(target_id) is not None:
                        server = x
                        break
            channel = self.bot.get_channel(id=target_id)
            member = server.get_member(user_id=target_id)
            await self.bot.say("SERVER: **{}**\nCHANNEL: **{}**\nMEMBER: **{}**".format(server, channel, member))
        else:
            await self.bot.say("You do not have permission to use that command.")

    @commands.command(pass_context=True, hidden=True)
    async def close(self, ctx):
        """Ternminate Kamikaze."""
        if checks.check_owner(ctx.message):
            await self.bot.say('Bye Teitoku~')
            await self.bot.close()

    @commands.command(pass_context=True, hidden=True)
    async def change_profile_name(self, ctx, new_name : str):
        """Change Kamikaze's profile name"""
        if checks.check_owner(ctx.message):
            await self.bot.edit_profile(username=new_name)

    @commands.command(pass_context=True, hidden=True)
    async def status(self, ctx, *, new_status : str):
        """Change Kamikaze's status message."""
        if checks.check_owner(ctx.message):
            kamikaze_status = []
            kamikaze_status.append(new_status)
            await self.bot.change_presence(game=discord.Game(name=kamikaze_status[0]))
            with open('kamikaze_status.pickle', 'wb') as f:
                pickle.dump(kamikaze_status, f)

    @commands.command(name='say', pass_context=True, hidden=True)
    async def _say(self, ctx, channel_id : str, *, msg : str):
        """Get Kamikaze to output a message. Requires Administrator permission."""
        if checks.check_owner(ctx.message) or checks.check_admin(ctx.message):
            await self.bot.send_message(discord.Object(id=str(channel_id)), msg)
            await self.bot.delete_message(ctx.message)

    @commands.command(name='type', pass_context=True, hidden=True)
    async def _type(self, ctx, channel_id : str, *, msg : str):
        """Get Kamikaze to type and send a message to a channel."""
        if checks.check_owner(ctx.message):
            await self.bot.delete_message(ctx.message)
            await self.bot.send_typing(self.bot.get_channel(channel_id))
            await asyncio.sleep(len(msg) / 7)
            await self.bot.send_message(self.bot.get_channel(channel_id), msg)

    @commands.command(pass_context=True, hidden=True)
    async def stylish_say(self, ctx, channel_id : str, *, msg : str):
        """Get Kamikaze to type and send a message to a channel using embeds."""
        if checks.check_owner(ctx.message):
            await self.bot.delete_message(ctx.message)
            await self.bot.send_typing(self.bot.get_channel(channel_id))
            await asyncio.sleep(len(msg) / 7)
            await self.bot.send_message(self.bot.get_channel(channel_id), embed=tools.createEmbed(title=msg))

    @commands.command(pass_context=True)
    async def clean(self, ctx, msg_amount=40):
        """Purges command messages and Kamikaze's outputs from the channel."""
        if checks.check_moderator(ctx.message):
            predicate = lambda m: m.author == self.bot.user or m.content.startswith('!k.')
            deleted = await self.bot.purge_from(ctx.message.channel, limit=msg_amount+1, check=predicate)
            await asyncio.sleep(1)
            await self.bot.say("Deleted {} message(s).".format(len(deleted)-1), delete_after=6)

    @commands.command(name="list", pass_context=True)
    async def _list(self, ctx):
        """View a list of Kamikaze's available cogs."""
        if checks.check_admin(ctx.message):
            unInstalledCogs = str([x for x in os.listdir(".\cogs") if x.endswith(".py") and x[:-3] not in (cog.lower() for cog in self.bot.cogs)]).strip('[]').replace("'","").replace(".py", "")
            installedCogs = str([x for x in self.bot.cogs]).strip('[]').replace("'","")
            title = "Kamikaze's Cog Information"
            description ="**Installed cogs:\n**" + installedCogs + "\n\n**Uninstalled cogs:**\n" + unInstalledCogs
            em = tools.createEmbed(title, description)
            await self.bot.say(embed=em)
            #await self.bot.say("Here's my currently installed modules ( ;・w・)7\n```{}```".format(cogsList)) #dont forget to replace them later

    @commands.command(pass_context=True)
    async def mute(self, ctx, user_id : str):
        """Prevent a member on Hourai from sending messages or speaking. Use again to undo."""
        server = ctx.message.server
        if checks.check_teitoku(ctx.message):
            user = server.get_member(user_id)
            if user is not None:
                # Get muted role
                muted_role = discord.utils.get(server.roles, id="476274041154437123")
                # Check if user does not have the "muted" role
                if muted_role not in user.roles:
                    await self.bot.add_roles(user, muted_role)
                    await self.bot.say("{} has been muted. Please take this time to cool and reflect.".format(user.mention))
                else:
                    # User has the role, so unmute
                    await self.bot.remove_roles(user, muted_role)
                    await self.bot.say("{} has been unmuted. Welcome back!".format(user.mention))
            else:
                # User is none, so user not found
                await self.bot.say("Could not find a user with such an ID.")

    @commands.group(pass_context=True, aliases=["roles"])
    async def role(self, ctx):
        """Assign (or unassign) yourself a role. Use `add` or `remove` subcommand to edit assignable roles. For Hourai only."""
        if not checks.check_hourai(ctx.message):
            await self.bot.say("This command can only be used in **Houraigekisen, Yoi!**")
            return
        if ctx.invoked_subcommand is None:
            # Display a list of self-assignable roles.
            try:
                role_list = tools.loadPickle("assignable_roles.pickle")
            except FileNotFoundError:
                await self.bot.say("There are currently no self-assignable roles.")
                return
            role_list_names = [role.name for role in role_list]
            if role_list_names != []:
                await self.bot.say(embed=tools.createEmbed(title="Self-assignable Roles", description="\n".join(role_list_names)))
            else:
                await self.bot.say("There are currently no self-assignable roles.")

    @role.command(pass_context=True)
    async def enable(self, ctx, *, role : str):
        """Allow other users to assign themselves this role."""
        if not checks.check_admin(ctx.message):
            await self.bot.say("You do not have permission to do that.")
            return
        server_roles = ctx.message.server.roles
        # Find discord role by name or ID
        discord_role = tools.getByIdOrName(server_roles, role)
        if discord_role is None:
            await self.bot.say("Could not find role **{}**. Please make sure the ID or Role name is correct.".format(role))
            return
        # Role found. Do not add role if Default or higher.
        DEFAULT_ROLE = discord.utils.get(server_roles, name="Default")
        if discord_role >= DEFAULT_ROLE:
            await self.bot.say("**{}'s** role hierarchy order is too high to enable self-assignment.".format(discord_role.name))
            return
        ROLE_PICKLE = "assignable_roles.pickle"
        try:
            role_list = tools.loadPickle(ROLE_PICKLE)
            if discord_role in role_list:
                await self.bot.say("**{}** has already been set as assignable.".format(discord_role.name))
                return
            else:
                role_list.append(discord_role)
                tools.dumpPickle(role_list, ROLE_PICKLE)
        except FileNotFoundError:
            # Create role list pickle
            tools.dumpPickle([discord_role], ROLE_PICKLE)
        await self.bot.say("**{}** set as assignable.".format(discord_role.name))

    @role.command(pass_context=True)
    async def disable(self, ctx, *, role : str):
        """Remove a role from the list of self-assignable roles."""
        if not checks.check_admin(ctx.message):
            await self.bot.say("You do not have permission to do that.")
            return
        ROLE_PICKLE = "assignable_roles.pickle"
        try:
            role_list = tools.loadPickle(ROLE_PICKLE)
        except FileNotFoundError:
            await self.bot.say("No roles have been added to the self-assignable roles list.")
            return
        server_roles = ctx.message.server.roles
        # Attempt to find the role in server by ID or name
        discord_role = tools.getByIdOrName(server_roles, role)
        if discord_role is None:
            await self.bot.say("Could not find role **{}**. Please make sure the ID or Role name is correct".format(role))
            return
        # Role found
        if discord_role not in role_list:
            # Role exists in server but not in assignable list.
            await self.bot.say("**{}** has not been added to the self-assignable roles list.".format(discord_role.name))
            return
        # Remove the role
        role_list.remove(discord_role)
        tools.dumpPickle(role_list, ROLE_PICKLE)
        await self.bot.say("**{}** has been removed from the list.".format(discord_role.name))

    @role.command(pass_context=True)
    async def add(self, ctx, *, role : str):
        """Assign yourself a role."""
        ROLE_PICKLE = "assignable_roles.pickle"
        role_list = tools.loadPickle(ROLE_PICKLE)
        discord_role = tools.getByIdOrName(role_list, role)
        if discord_role is None:
            await self.bot.say("**{}** was not found in the role list. Please check your spelling and use `!k.role` to view the list of self-assignable roles.".format(role))
            return
        else:
            author = ctx.message.author
            if discord_role in author.roles:
                await self.bot.say("{} already has the role **{}**.".format(author.name, discord_role.name))
                return
            await self.bot.add_roles(author, discord_role)
            await self.bot.say("Successfully gave **{}** to {}.".format(discord_role.name, author.name))

    @role.command(pass_context=True)
    async def remove(self, ctx, *, role : str):
        """Remove a role assigned to you."""
        ROLE_PICKLE = "assignable_roles.pickle"
        role_list = tools.loadPickle(ROLE_PICKLE)
        discord_role = tools.getByIdOrName(role_list, role)
        if discord_role is None:
            await self.bot.say("**{}** was not found in the role list. Please check your spelling and use `!k.role` to view the list of self-assignable roles.".format(role))
            return
        else:
            author = ctx.message.author
            if discord_role not in author.roles:
                await self.bot.say("{} does not have the role **{}**.".format(author.name, discord_role.name))
                return
            await self.bot.remove_roles(author, discord_role)
            await self.bot.say("Successfully removed **{}** from {}.".format(discord_role.name, author.name))

    @commands.command(pass_context=True, hidden=True)
    async def _serverSetup(self, ctx):
        """Setup server specific persistence modules."""
        if checks.check_owner(ctx.message) or checks.check_admin(ctx.message):
            serverID = ctx.message.server.id
            await self.bot.delete_message(ctx.message)
            await self.bot.say("Setting up...", delete_after=12)
            try:
                #kamikaze chime
                kamikaze_chime = tools.loadPickle('kamikaze_chime.pickle')
                kamikaze_chime[serverID] = True
                tools.dumpPickle(kamikaze_chime, 'kamikaze_chime.pickle')
                await self.bot.say("**kamikaze_chime** setup success", delete_after=10)
                # END
                await self.bot.say("Setup successful", delete_after=10)
            except Exception as e:
                await self.bot.say("SETUP FAILED\n{}: {}".format(type(e).__name__, e))

    ## UTILITY COMMANDS
    @commands.command(pass_context=True, hidden=True)
    async def cls(self, ctx):
        """Pseudo cls on std_out."""
        if checks.check_owner(ctx.message):
            print('\n'*10)

def setup(bot):
    bot.add_cog(Admin(bot))
