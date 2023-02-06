import asyncio
import os
import discord
from discord.ext import commands
import random
import time
from datetime import datetime

# get token from file token.txt within the same directory as this script
token=''
with open('token.txt') as token_file:
    token = token_file.readline()[:-1]
    
# disable video on ffpmeg since it isn't necessary 
ffmpeg_options = {
    'options': '-vn'
}

# sound_dir is a directory containing your normalized audio clips, change it as needed
sound_dir = 'audio_clips_normalized/'

# some lists used by features of this bot
# bot_join_list: audio to choose from when the bot joins a voice channel
# bot_leave_list: audio to choose from when the bot leaves a voice channel
# people_join_list: audio to choose from when people join a voice channel
# people_leave_list: audio to choose from when people leave a voice channel
bot_join_list = ['bot_join1.mp3','bot_join2.mp3']
bot_leave_list = ['bot_leave.mp3']
people_join_list = ['people_join.mp3']
people_leave_list = ['people_leave.mp3']

# initialize the bot through the discord API giving it all the intents (if you're worried about 
# security you might want to edit the intents of the bot, at minimum it needs to connect/speak
# in voice channels and read/write in text channels)
intents = discord.Intents().all()
bot = commands.Bot(command_prefix=commands.when_mentioned_or("~"), description='Sound board bot',intents=intents)

# remove the help command because it gets replaced by a custom help command
bot.remove_command('help')

# construct a formatted string to print when called by commands
sounds_list = os.listdir(sound_dir)
sounds_list_str = ""
max_index_str_len = len(str(len(sounds_list)))
for i in range(0, len(sounds_list)):
    # add spaces in front of index to right allign column
    for j in range(len(str(i + 1)),max_index_str_len):
        sounds_list_str += ' '
    sounds_list_str += str(i + 1) + ':' + '\t' 
    sounds_list_str += sounds_list[i][0:-4]
    sounds_list_str += '\n'


async def randomtime():
    """
    play a random audio clip
    """
    if bot.voice_clients:
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio('sounds/' + random.choice(sounds_list)))
        bot.voice_clients[0].play(source, after=lambda e: print('Player error: %s' % e) if e else None)
        print('random clip played at {0}'.format(datetime.now().strftime("%H:%M:%S")))
    else:
        print('no random clip played at {0}, bot was not in a voice channel'.format(datetime.now().strftime("%H:%M:%S")))


class Audio(commands.Cog):
    """
    audio class containing main functions of this bot
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx):
        """
        command for the bot to join the current channel you're in. the bot can also wsitch to your
        channel if you call join
        """
        print('{0} called join at {1}'.format(ctx.author, datetime.now().strftime("%H:%M:%S")))
        # if the bot is in another voice channel then switch channels
        channel = ctx.author.voice.channel
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        # join and play a sound from the join list
        await channel.connect()
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(sound_dir + random.choice(bot_join_list)))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

    @commands.command()
    async def play(self, ctx, *, query):
        """
        command to play a specified audio clip,
        can only be done from the channel you are in,
        tell user to check list if the audio clip doesn't exist
        """
        if ctx.author.voice is None or ctx.author.voice.channel.id != bot.voice_clients[0].channel.id:
            await ctx.send('you are not in the right channel')
        else:
            print('{0} called play at {1}'.format(ctx.author, datetime.now().strftime("%H:%M:%S")))
            # play an audio clip based on its 1 based index in the list
            if query[0] == '#':
                try:
                    print(query[1:])
                    num = int(query[1:])
                    if num < 1:
                        raise Exception()
                    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(sound_dir + sounds_list[num - 1]))
                    ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
                    await ctx.send('Now playing: {}'.format(sounds_list[num - 1][:-4]))
                except:
                    await ctx.send('{} is not a valid number\ntype \"~list\" for more info'.format(query))
            # play an audio clip based on its name
            elif query + '.mp3' in sounds_list:
                source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(sound_dir + query + '.mp3'))
                ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
                await ctx.send('Now playing: {}'.format(query))
            else:
                await ctx.send('{} is not a valid sound or number\ntype \"~list\" for more info'.format(query))

    @commands.command()
    async def stop(self, ctx):
        """
        command to stop an audio clip while its playing
        """
        print('{0} called stop at {1}'.format(ctx.author, datetime.now().strftime("%H:%M:%S")))
        ctx.voice_client.stop()

    @commands.command()
    async def leave(self, ctx):
        """
        command to leave the voice channel
        """
        print('{0} called leave at {1}'.format(ctx.author, datetime.now().strftime("%H:%M:%S")))
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(sound_dir + random.choice(bot_leave_list)))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
        # wait for audio to finish playing then disconect
        while ctx.voice_client.is_playing():
            time.sleep(0.1)
        await ctx.voice_client.disconnect()
        
    @commands.command()
    async def list(self, ctx):
        """
        command to list out all audio clips along with their index
        """
        print('{0} called list at {1}'.format(ctx.author, datetime.now().strftime("%H:%M:%S")))
        await ctx.send("```\nAudio clips\n\n{}\n```".format(sounds_list_str))
        
    @commands.command()
    async def find(self, ctx, *, query):
        """
        command to search for audio clips from the list
        only exact substrings will return results
        """
        found = ""
        for i in range(0, len(sounds_list)):
            if query in sounds_list[i]:
                if i < 9:
                    found += ' '
                found += str(i + 1) + ':' + '  ' 
                found += sounds_list[i][0:-4]
                found += '\n'
        print('{0} called find {2} at {1}'.format(ctx.author, datetime.now().strftime("%H:%M:%S"), query))
        if len(found) == 0:
            await ctx.send('could not find {}'.format(query))
        else:
            await ctx.send("```\nResults\n\n{}\n```".format(found))
        
    @commands.command()
    async def random(self, ctx):
        """
        command to randomly choose an audio clip and play it
        """
        if ctx.author.voice is None or ctx.author.voice.channel.id != bot.voice_clients[0].channel.id:
            await ctx.send('you are not in the right channel')
        else:
            print('{0} called random at {1}'.format(ctx.author, datetime.now().strftime("%H:%M:%S")))
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(sound_dir + random.choice(sounds_list)))
            ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

    @commands.command()
    async def help(self, ctx):
        """
        command to print help information
        """
        print('{0} called help at {1}'.format(ctx.author, datetime.now().strftime("%H:%M:%S")))
        await ctx.send("""
```
~join:                      join channel
~play [sound or #number]:   play sound
~stop:                      stops playing current sound
~random:                    chooses a random sound
~leave:                     kicks bot from voice channel
~list:                      displays list of all sounds
~find [query]:              finds all sounds with query

play uasge examples:
~play hello
or 
~play #2
```
""")

    @play.before_invoke
    @random.before_invoke
    @leave.before_invoke
    @stop.before_invoke
    async def ensure_voice(self, ctx):
        """
        helper function to ensure that the bot is connected to voice before commands
        that interact with audio are called
        """
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

@bot.event
async def on_ready():
    """
    start a timer loop when bot is launched to randomly play a sound every 30-90 min 
    if its in a voice channel
    """
    print('Logged in as {0} ({0.id})'.format(bot.user))
    print('------')
    await bot.add_cog(Audio(bot))
    while True:
        ran = random.randint(30 * 60,90 * 60)
        print("next randomtime in: {0}".format(time.strftime('%H:%M:%S', time.gmtime(ran))))
        await asyncio.sleep(ran)
        await randomtime()

@bot.event
async def on_voice_state_update(member, before, after):
    """
    when people join or leave the voice channel triggers the bot to play specific audio clips
    """
    try:
        # if the bot isn't in a channel do nothing
        if not bot.voice_clients:
            return
        # if there are no changes to channel do nothing (as in if someone mutes it won't trigger)
        elif before.channel is not None and after.channel is not None and before.channel == after.channel:
            return
        # if no more people are in the channel the bot leaves
        elif len(bot.voice_clients[0].channel.members) == 1:
            print('bot left at {0} no more people'.format(datetime.now().strftime("%H:%M:%S")))
            await bot.voice_clients[0].disconnect()
        # if someone joins then play a specific audio clip
        elif after.channel is not None and after.channel.id == bot.voice_clients[0].channel.id:
            if before.channel is None:
                source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(sound_dir + random.choice(people_join_list)))
                bot.voice_clients[0].play(source, after=lambda e: print('Player error: %s' % e) if e else None)
            elif before.channel.id != after.channel.id:
                source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(sound_dir + random.choice(people_join_list)))
                bot.voice_clients[0].play(source, after=lambda e: print('Player error: %s' % e) if e else None)
        # if someone leaves then play a specific audio clip
        elif before.channel is not None and before.channel.id == bot.voice_clients[0].channel.id:
            if after.channel is None:
                source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(sound_dir + random.choice(people_leave_list)))
                bot.voice_clients[0].play(source, after=lambda e: print('Player error: %s' % e) if e else None)
            elif before.channel.id != after.channel.id:
                source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(sound_dir + random.choice(people_leave_list)))
                bot.voice_clients[0].play(source, after=lambda e: print('Player error: %s' % e) if e else None)
    except:
        print('exeption in on_voice_state_update at {}'.format(datetime.now().strftime("%H:%M:%S")))

bot.run(token)