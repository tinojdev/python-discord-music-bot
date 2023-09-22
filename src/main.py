from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(".env"))

import logging
import discord
import os
import asyncio

from discord.ext import commands


from command_handler import CommandHandler
from event_handler import EventHandler
from temp_handler import TempHandler
from task_runner import TaskRunner


intents = discord.Intents.default()
intents.guilds = True
intents.guild_messages = True
intents.voice_states = True
intents.message_content = True


def get_prefix(*_):
    return "!"


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    BOT_TOKEN = os.getenv("DISCORD_TOKEN")

    if not BOT_TOKEN:
        raise RuntimeError("DISCORD_TOKEN environment variable is not set.")

    TempHandler.clear_temp_dir()

    bot = commands.Bot(command_prefix=get_prefix, intents=intents)
    async with bot:
        await bot.add_cog(EventHandler(bot))
        await bot.add_cog(CommandHandler(bot))
        await bot.add_cog(TaskRunner(bot))
        await bot.start(BOT_TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
