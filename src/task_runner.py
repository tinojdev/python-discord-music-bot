import logging

from discord.ext import commands, tasks

from temp_handler import TempHandler

logger = logging.getLogger(__name__)


class TaskRunner(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.remove_old_temp_files.start()

    @tasks.loop(seconds=60 * 15)
    async def remove_old_temp_files(self):
        TempHandler.delete_all_to_delete_files()
