import discord, asyncio
from discord.ext import commands
from cogs.utilities import tools
from apiclient.discovery import build
from apiclient.errors import HttpError

API_KEY = tools.loadPickle('youtube_api_key.pickle')
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

SELECTION_TIMEOUT = 300 # 5 minutes

def youtube_search(q):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)
    search_response = youtube.search().list(q=q, type="video", part="snippet", maxResults=9).execute()
    videos = []
    for item in search_response['items']:
        videos.append((item['id']['videoId'], item['snippet']['title']))
    return videos # returns a list of (ID, VIDEO_TITLE)

async def display_choices(bot, ctx, options, query : str):
    title = "Results for: _{}_".format(query)
    description = "Please select an option:\n\n"
    description += '\n'.join(["**{}.** {}".format(options.index(x) + 1, x[1]) for x in options])
    description += "\n\n**c.** cancel"
    em = tools.createEmbed(title=title, description=description)
    selections = await bot.send_message(ctx.message.channel, embed=em)
    msg = await bot.wait_for_message(timeout=SELECTION_TIMEOUT, author=ctx.message.author, check=lambda x: x.content.lower() in ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'c'])
    if msg is None:
        await bot.send_message(ctx.message.channel, "{}, your selection has timed out.".format(ctx.message.author.mention))
        await bot.delete_message(selections)
        return
    elif msg.content.lower() == "c":
        await bot.say("Selection cancelled.")
        await bot.delete_messages([msg, selections])
    else:
        await bot.delete_messages([msg, selections])
        # return video URL
        return "https://www.youtube.com/watch?v={}".format(options[int(msg.content) - 1][0])

class Music:

    def __init__(self, bot):
        self.bot = bot
        self.players = {}

    @commands.command(pass_context=True)
    async def join(self, ctx):
        """Get Kamikaze to join the voice channel you are in."""
        if not self.bot.is_voice_connected(ctx.message.server):
            if ctx.message.author.voice.voice_channel is None:
                # if the user isn't in any voice channel:
                await self.bot.say("You are not connected to any voice channel...")
            else:
                # if user is connected to a voice channel and bot is not in a voice channel already:
                voice_client = await self.bot.join_voice_channel(ctx.message.author.voice.voice_channel)
                # Note: no player is created upon join. A song must be played for a player to be registered to self.player
        else:
            await self.bot.say("I am already connected to a voice channel...")

    @commands.command(pass_context=True)
    async def leave(self, ctx):
        """Get Kamikaze to leave the voice channel she is connected in"""
        server = ctx.message.server
        if self.bot.is_voice_connected(server):
            voice_client = self.bot.voice_client_in(server)
            await self.bot.say("Disconnecting from {}".format(voice_client.channel.name))
            await voice_client.disconnect()
            try:
                self.players.pop(server.id)
            except KeyError:
                pass
        else:
            await self.bot.say("Not connected to any voice channel...")

    @commands.command(pass_context=True)
    async def play(self, ctx, *, url : str):
        """Get Kamikaze to play a song"""
        server = ctx.message.server
        if self.bot.is_voice_connected(server):
            voice_client = self.bot.voice_client_in(server)
            try:
                self.players[server.id].stop()
            except KeyError:
                pass
            if '/watch?v=' in url:
                self.players[server.id] = await voice_client.create_ytdl_player(url)
            else:
                # if player did not enter a URL:
                try:
                    search_results = youtube_search(url)
                except HttpError as e:
                    await self.bot.say("An HTTP error {} occurred: {}".format(e.resp.status, e.content))
                selection = await display_choices(self.bot, ctx, search_results, url)
                if selection is None:
                    return
                else:
                    self.players[server.id] = await voice_client.create_ytdl_player(selection)
            await asyncio.sleep(1) # sleep required to not skip first second of song
            self.players[server.id].start()
            await self.bot.delete_message(ctx.message)
            await self.bot.say("Playing **{}**".format(self.players[server.id].title))
        else:
            await self.bot.say("Not connected to any voice channel...")

    @commands.command(pass_context=True)
    async def pause(self, ctx):
        """Pause the currently playing song"""
        server = ctx.message.server
        try:
            if self.players[server.id].is_playing():
                self.players[server.id].pause()
                await self.bot.say("Paused.")
            else:
                await self.bot.say("Currently not playing anything...")
        except KeyError:
            await self.bot.say("Currently not connected to any voice channel.")

    @commands.command(pass_context=True)
    async def resume(self, ctx):
        """Resume the currently playing song"""
        server = ctx.message.server
        try:
            if not self.players[server.id].is_done():
                self.players[server.id].resume()
                await self.bot.say("Resumed.")
            else:
                await self.bot.say("Currently not playing anything...")
        except KeyError:
            await self.bot.say("Currently not connected to any voice channel.")

    @commands.command(pass_context=True)
    async def stop(self, ctx):
        """Stop playing the current song"""
        server = ctx.message.server
        try:
            if self.players[server.id].is_playing():
                self.players[server.id].stop()
                await self.bot.say("Stopped playing **{}**".format(self.players[server.id].title))
            else:
                await self.bot.say("Currently not playing anything...")
        except KeyError:
            await self.bot.say("Currently not connected to any voice channel.")

    @commands.command(pass_context=True)
    async def np(self, ctx):
        """Get the currently playing song's title"""
        server = ctx.message.server
        try:
            if not self.players[server.id].is_done():
                await self.bot.say("Currently playing **{}**".format(self.players[server.id].title))
            else:
                await self.bot.say("Currently not playing anything...")
        except KeyError:
            await self.bot.say("Currently not conencted to any voice channel.")

def setup(bot):
    bot.add_cog(Music(bot))