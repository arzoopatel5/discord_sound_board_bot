# Discord Sound Board Bot
A discord bot designed to act like a sound board. Its main function is to join voice channels and play audio clips on demand.

# Prerequisites
  - [discord bot](https://discord.com/developers/docs/intro)
  - [WSL](https://ubuntu.com/wsl) (or another way of running bash if you're using windows) with the following
    - [miniconda](https://docs.conda.io/en/latest/miniconda.html) (or anaconda) with the following in an environment named `discord`
      - python 3.10.8
      - [discord.py](https://discordpy.readthedocs.io/en/stable/) 2.1.0
      - [ffmpeg](https://ffmpeg.org/) 5.1.2
      - [ffmpeg-normalize](https://docs.conda.io/en/latest/miniconda.html) 1.26.1

Version numbers provided for reference. Exact versions may not be necessary.

# Setup
Required
 - Clone this github repo
 - Create a [discord bot](https://discord.com/developers/docs/intro) and give it [Privileged Gateway Intents](https://discord.com/developers/docs/topics/gateway#gateway-intents)
 - Add it to your discord server
 - In `token.txt` replace the 0's with your bot's token
 - In `audio_clips_unnormalized` place your audio clips in mp3 format
 - In `discord_sound_board_bot.py` on lines 27-30 replace the dummy files with names of files you want for each purpose
 - In `launch.bat` edit the path to be the folder that contains the bot
   - This should be in linux format
 - In `launch.sh` on line 6 use the same path as above
 - Find your `conda.sh` and put the path in `launch.sh` on line 3 (its most likely in `/home/<username>/miniconda3/etc/profile.d/conda.sh`)

Optional (for windows)
 - Add `launch.bat` to your startup
 - `win + R` and type `shell:startup` and place the file here
 - This makes it so the bot launches whenever you turn on your PC

You should be able to launch the bot now by running `launch.bat`. It will take a while on first launch because it will normalize all your audio. If you have more audio clips to add later just drop them in the `audio_clips_unnormalized` folder and the script will handle the rest.

# Commands
Commands can be called using `~` followed by a command
  - `~help` lists commands with simple descriptions
  - `~list` lists all audio clips with an index that can be used with the `~play` command
  - `~find` searches for a query in the audio clips and returns a list of matches
  - `~join` calls the bot into the user's current voice channel. The bot will choose a random greeting from `bot_join_list`
  - `~leave` tells the bot to leave the user's current voice channel. The bot will choose a random farewell from `bot_leave_list`
  - `~play` tells the bot to play a specified audio clip. The user can also use `#` followed by the index from `~list` or `~find`
  - `~random` tells the bot to play a random audio clip
  - `~stop` tells the bot to stop playing

# Additional Features
  - The bot will also leave when everyone else leaves the voice channel
  - When a user joins a channel the bot is in, the bot will greet them choosing randomly from `people_join_list`
  - When a user leaves a channel, the bot will choose randomly from `people_leave_list`
