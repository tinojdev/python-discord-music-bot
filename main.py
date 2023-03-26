import logging
import discord
import os
import asyncio

from discord.ext import commands
from dotenv import load_dotenv, find_dotenv

from src.command_handler import CommandHandler
from src.event_handler import EventHandler
from src.temp_handler import TempHandler
from src.task_runner import TaskRunner

load_dotenv(find_dotenv(".env"))

BOT_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.guilds = True
intents.guild_messages = True
intents.voice_states = True
intents.message_content = True


def get_prefix(_bot, _message):
    return "!"


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = commands.Bot(command_prefix=get_prefix, intents=intents)


async def main():
    TempHandler.clear_temp_dir()
    async with bot:
        await bot.add_cog(EventHandler(bot))
        await bot.add_cog(CommandHandler(bot))
        await bot.add_cog(TaskRunner(bot))
        await bot.start(BOT_TOKEN)


if __name__ == '__main__':
    asyncio.run(main())
