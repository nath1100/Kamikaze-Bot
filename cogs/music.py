import discord
from discord.ext import commands

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
        else:
            await self.bot.say("I am already connected to a voice channel...")

    @commands.command(pass_context=True)
    async def leave(self, ctx):
        """Get Kamikaze to leave the voice channel she is connected in"""
        if self.bot.is_voice_connected(ctx.message.server):
            voice_client = self.bot.voice_client_in(ctx.message.server)
            await self.bot.say("Disconnecting from {}".format(voice_client.channel.name))
            await voice_client.disconnect()
        else:
            await self.bot.say("Not connected to any voice channel...")

    @commands.command(pass_context=True)
    async def play(self, ctx, *, url : str):
        """Get Kamikaze to play a song"""
        server = ctx.message.server
        if self.bot.is_voice_connected(server):
            voice_client = self.bot.voice_client_in(server)
            self.players[server.id] = await voice_client.create_ytdl_player(url)
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
            else:
                await self.bot.say("Currently not playing anything...")
        except KeyError:
            await self.bot.say("Currently not connected to any voice channel.")

def setup(bot):
    bot.add_cog(Music(bot))