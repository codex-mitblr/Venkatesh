from disnake.ext import commands

from ...constants import Roles


class BotRepeats(commands.Cog):
    """Announcements made using the bot."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(3, 15)
    @commands.has_any_role(Roles.moderator)
    async def repeat(self, ctx: commands.Context, *, message: str) -> None:
        """Returns the message specified by the user."""
        await ctx.message.delete()
        await ctx.send(message, allowed_mentions=None)


def setup(bot: commands.Bot) -> None:
    """Loads the BotRepeats cog."""
    bot.add_cog(BotRepeats(bot))
