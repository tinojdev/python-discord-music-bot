## Discord music bot

This is a music bot for discord. It is written in python and uses the discord.py library.

Originally written in Typescript but now ported to python because npm libraries have a habit of not working.

## Setup

- Download and install ffmpeg
- Add a .env file with the following contents:

```
DISCORD_TOKEN=your_token_here
TEMP_DIR=/path/to/temp/dir # this is where the bot will store temporary music files
```

- Run **python main.py**