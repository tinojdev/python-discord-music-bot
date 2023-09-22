import logging
from discord.ext.commands import Cog, Bot

logger = logging.getLogger(__name__)


class EventHandler(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if self.bot.user:
            print(f"Logged in as {self.bot.user} (ID: {self.bot.user.id})")

    @Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        return

    @Cog.listener()
    async def on_command_error(self, ctx, error):
        logger.error(error)

        await ctx.send(error)
        raise error
