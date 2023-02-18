from datetime import datetime

from disnake import Embed, Member, Message, TextChannel
from disnake.ext import commands
from loguru import logger

from ...constants import Channels, Colors


class JoinLeaveLog(commands.Cog):
    """Log members joining and leaving."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.member_log: TextChannel | None = None
        super().__init__()

    async def post_message(self, embed: Embed) -> Message | None:
        """Send the given message in the joins-and-leaves channel."""
        if self.member_log is None:
            await self.bot.wait_until_ready()
            self.member_log = await self.bot.fetch_channel(Channels.memberlog)

            if self.member_log is None:
                logger.error(
                    f"Failed to get log channel with ID ({Channels.memberlog})"
                )

        return await self.member_log.send(embed=embed)

    async def post_formatted_message(
        self,
        member: Member,
        title: str,
        description: str,
        footer: str,
        color: int = Colors.green,
    ) -> None:
        """Formats the log message into an embed."""
        embed = Embed(
            title=title, description=description, color=color, timestamp=datetime.now()
        )

        embed.set_author(
            name="Team CodeX",
            icon_url="https://codex.mitb.club/brand_enlarged.png",
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text=footer)

        await self.post_message(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member: Member) -> None:
        """Logs new members joining the server."""
        await self.post_formatted_message(
            member=member,
            title=f"{member.name} Joined!",
            description=f"{member.mention}, welcome to **CodeX**! "
            "We hope you have a great time here. Please go through "
            f"{(await self.bot.fetch_channel(Channels.rules)).mention} in order to proceed.",
            footer=f"{member.guild.member_count} Members",
        )

    @commands.Cog.listener()
    async def on_member_remove(self, member: Member) -> None:
        """Logs members leaving the server."""
        await self.post_formatted_message(
            member=member,
            title=f"{member.display_name} Left",
            description="We hope you enjoyed your time here.",
            footer=f"{member.guild.member_count} Members",
            color=Colors.orange,
        )


def setup(bot: commands.Bot) -> None:
    """Loads the JoinLeaveLog cog."""
    bot.add_cog(JoinLeaveLog(bot))
