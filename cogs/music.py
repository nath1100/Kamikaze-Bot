import discord, asyncio, time
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
        selected_id = int(msg.content) - 1
        return ("https://www.youtube.com/watch?v={}".format(options[selected_id][0]), options[selected_id][1]) # (video URL, video title)

class Music:
    """Commands for music control in voice channels."""

    def __init__(self, bot):
        self.bot = bot
        self.players = {}
        self.queues = {}
        self.sample_rate = 48000

    async def process_queue(self, ctx):
        voice_client = self.bot.voice_client_in(ctx.message.server)
        server_id = ctx.message.server.id
        self.players[server_id] = await voice_client.create_ytdl_player(self.queues[server_id].pop(0), after=lambda: asyncio.run_coroutine_threadsafe(self.process_queue(ctx), self.bot.loop).result())
        self.players[server_id].volume = 0.1 #set player volume to 10%
        #self.players[server_id] = self.queues[server_id].pop(0)
        await asyncio.sleep(3)
        self.players[server_id].start()
        length_seconds = divmod(self.players[server_id].duration, 60)
        song_length = "{}:{:02d}".format(length_seconds[0], length_seconds[1])
        await self.bot.send_message(ctx.message.channel, "Playing **{}** _{}_".format(self.players[server_id].title, song_length))

    @commands.command(pass_context=True, no_pm=True)
    async def join(self, ctx):
        """Get Kamikaze to join the voice channel you are connected to."""
        server = ctx.message.server
        if not self.bot.is_voice_connected(ctx.message.server):
            if ctx.message.author.voice.voice_channel is None:
                # if the user isn't in any voice channel:
                await self.bot.say("You are not connected to any voice channel.")
            else:
                # if user is connected to a voice channel and bot is not in a voice channel already:
                # initialise
                if server.id not in self.queues:
                    self.queues[server.id] = []
                voice_client = await self.bot.join_voice_channel(ctx.message.author.voice.voice_channel)
                voice_client.encoder_options(sample_rate=self.sample_rate)
                # Note: no player is created upon join. A song must be played for a player to be registered to self.player
        else:
            await self.bot.say("I am already connected to a voice channel.")

    @commands.command(pass_context=True, no_pm=True)
    async def leave(self, ctx):
        """Get Kamikaze to leave the voice channel she is connected to."""
        server = ctx.message.server
        if self.bot.is_voice_connected(server):
            voice_client = self.bot.voice_client_in(server)
            await self.bot.say("Disconnecting from {}".format(voice_client.channel.name))
            # clear the queue
            try:
                self.queues[server.id] = []
                self.players[server.id].stop()
            except KeyError:
                pass
            await voice_client.disconnect()
            try:
                self.players.pop(server.id)
            except KeyError:
                pass
        else:
            await self.bot.say("Not connected to any voice channel.")

    @commands.command(pass_context=True, no_pm=True)
    async def play(self, ctx, *, url : str):
        """Get Kamikaze to play the audio from a Youtube video."""
        server = ctx.message.server
        if self.bot.is_voice_connected(server):
            #voice_client = self.bot.voice_client_in(server)
            ''' When !k.play is used, stop current song
            try:
                self.players[server.id].stop()
            except KeyError:
                pass
            '''
            if '/watch?v=' in url:
                    #self.players[server.id] = await voice_client.create_ytdl_player(url)
                    #self.queues[server.id].append(await voice_client.create_ytdl_player(url, after=lambda: asyncio.run_coroutine_threadsafe(self.process_queue(ctx), self.bot.loop).result()))
                    self.queues[server.id].append(url)
                    await self.bot.say("Added to queue.")
            else:
                # if player did not enter a URL:
                try:
                    search_results = youtube_search(url)
                except HttpError as e:
                    await self.bot.say("An HTTP error {} occurred: {}".format(e.resp.status, e.content))
                selection, title = await display_choices(self.bot, ctx, search_results, url)
                if selection is None:
                    return
                else:
                    #self.players[server.id] = await voice_client.create_ytdl_player(selection)
                    #self.queues[server.id].append(await voice_client.create_ytdl_player(selection, after=lambda: asyncio.run_coroutine_threadsafe(self.process_queue(ctx), self.bot.loop).result()))
                    self.queues[server.id].append(selection)
                    await self.bot.say("Added **{}** to the queue.".format(title))
            #await self.bot.say("Added **{}** to the queue.".format(self.queues[server.id][-1].title))
            #await self.bot.delete_message(ctx.message)
            '''
            await asyncio.sleep(1) # sleep required to not skip first second of song
            self.players[server.id].start()
            await self.bot.delete_message(ctx.message)
            length_seconds = divmod(self.players[server.id].duration, 60)
            song_length = "{}:{:02d}".format(length_seconds[0], length_seconds[1])
            await self.bot.say("Playing **{}** _{}_".format(self.players[server.id].title, song_length))
            '''
            try:
                if len(self.queues[server.id]) == 1 and self.players[server.id].is_done():
                    await self.process_queue(ctx)
            except KeyError:
                await self.process_queue(ctx)
        else:
            await self.bot.say("Not connected to any voice channel.")

    @commands.command(pass_context=True, no_pm=True)
    async def pause(self, ctx):
        """Pause the currently playing song."""
        server = ctx.message.server
        try:
            if self.players[server.id].is_playing():
                self.players[server.id].pause()
                await self.bot.say("Paused.")
            else:
                await self.bot.say("Currently not playing anything.")
        except KeyError:
            await self.bot.say("Currently not connected to any voice channel.")

    @commands.command(pass_context=True, no_pm=True)
    async def resume(self, ctx):
        """Resume the currently playing song."""
        server = ctx.message.server
        try:
            if not self.players[server.id].is_done():
                self.players[server.id].resume()
                await self.bot.say("Resumed.")
            else:
                await self.bot.say("Currently not playing anything.")
        except KeyError:
            await self.bot.say("Currently not connected to any voice channel.")

    @commands.command(pass_context=True, no_pm=True)
    async def skip(self, ctx):
        """Skip the currently playing song."""
        server = ctx.message.server
        try:
            if self.players[server.id].is_playing():
                self.players[server.id].stop()
                await self.bot.say("Skipped **{}**".format(self.players[server.id].title))
            else:
                await self.bot.say("Currently not playing anything.")
        except KeyError:
            await self.bot.say("Currently not connected to any voice channel.")

    ''' UNABLE TO RETRIEVE SONG TITLES AS PLAYER IS ONLY CREATED AFTER POPPING QUEUE
    MUST NOT CREATE EARLIER TO PREVENT PIPE BREAKAGES
    @commands.command(pass_context=True, no_pm=True)
    async def queue(self, ctx):
        """View the song queue."""
        server = ctx.message.server
        try:
            if self.queues[server.id] != []:
                songs = "\n".join([x.title for x in self.queues[server.id]])
                em = tools.createEmbed(title="Song list", description=songs)
                await self.bot.say(embed=em)
            else:
                await self.bot.say("No songs are in the queue.")
        except KeyError:
            await self.bot.say("No songs are in the queue.")
    '''

    @commands.command(pass_context=True, no_pm=True)
    async def np(self, ctx):
        """Get the currently playing song's title."""
        server = ctx.message.server
        try:
            if not self.players[server.id].is_done():
                length_seconds = divmod(self.players[server.id].duration, 60)
                song_length = "{}:{:02d}".format(length_seconds[0], length_seconds[1])
                await self.bot.say("Currently playing **{}** {}".format(self.players[server.id].title, song_length))
            else:
                await self.bot.say("Currently not playing anything.")
        except KeyError:
            await self.bot.say("Currently not conencted to any voice channel.")

    @commands.command(pass_context=True, no_pm=True)
    async def change_rate(self, ctx):
        """Change the sample rate of the music player. Match sample rate with the channel's bitrate for best results.
        Takes effect after rejoining the voice channel."""
        desc = "**1.** 8000\n**2.** 12000\n**3.** 16000\n**4.** 24000 (32kbps)\n**5.** 48000 (64kbps)\n\nCurrent rate: {}".format(self.sample_rate)
        rates = [None, 8000, 12000, 16000, 24000, 48000]
        em = tools.createEmbed(title="Select a sample rate", description=desc)
        selection = await self.bot.say(embed=em)
        msg = await self.bot.wait_for_message(timeout=30, author=ctx.message.author, check=lambda x: x.content in ['1', '2', '3', '4', '5'])
        if msg is None:
            await self.bot.delete_message(selection)
            return
        else:
            self.sample_rate = rates[int(msg.content)]
            await self.bot.say("Sample rate changed to {}.".format(rates[int(msg.content)]))

def setup(bot):
    bot.add_cog(Music(bot))
