#!/bin/bash

source /path/to/miniconda3/etc/profile.d/conda.sh 
conda activate discord

cd /path/to/discord/bot/directory/
ffmpeg-normalize -c:a libmp3lame -b:a 320k audio_clips_unnormalized/*.mp3 -of audio_clips_normalized -ofmt mp3 -ext mp3
python discord_sound_board_bot.py
