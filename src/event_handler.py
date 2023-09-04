from discord.ext.commands import Cog, Bot


class EventHandler(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        print(f"Logged in as {self.bot.user} (ID: {self.bot.user.id})")

    @Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        return

    @Cog.listener()
    async def on_command_error(self, ctx, error):
        await ctx.send(error)
