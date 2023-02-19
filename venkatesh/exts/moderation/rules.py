from disnake import Embed, File
from disnake.ext import commands

from ...constants import Colors, Roles


class Rules(commands.Cog):
    """Publish server rules in the specified channel."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(3, 30)
    @commands.has_any_role(Roles.moderator)
    async def rules(self, ctx: commands.Context) -> None:
        """Publishes rules embed in the channel."""
        rules_embed = Embed(
            title="Rules & Regulations",
            description="These rules have been put in place to ensure a safe environment for the CodeX "
            "community, and encourage healthy discussions. Moderation actions are taken"
            " on members accordingly.\n\n"
            "**1.** Treat everyone with respect, and express yourself in a constructive manner.\n"
            "**2.** Always follow the [Discord Terms of Service](https://dis.gd/terms) and"
            " [Community Guidelines](https://dis.gd/guidelines).\n"
            "**3.** Don't post NSFW/NSFL content, or content which is illegal or generally"
            " unsuitable for a development-type server.\n"
            "**4.** All channels have dedicated topics. Respect ongoing discussions in the"
            " channel and remain on-topic.",
            color=Colors.green,
        ).set_thumbnail(url="https://codex.mitb.club/brand_enlarged.png")
        rules_embed.set_author(
            name="Team CodeX",
            icon_url="https://codex.mitb.club/brand_enlarged.png",
        )

        community_embed = Embed(
            title="Community Guidelines",
            description="**1.** Don't spam messages or post emotes, which may cause issues for people"
            " with epilepsy.\n"
            "**2.** Discriminating or harassing other members is not allowed for any reason."
            " Do not send members of the community unsolicited DMs and/or friend requests.\n"
            "**3.** Media considered as violent or threatening that could cause"
            " discomfort (or worse) are prohibited.\n"
            "**4.** Impersonation of staff members is not allowed, under any circumstance.",
            color=Colors.green,
        ).set_thumbnail(file=File("venkatesh/assets/icon_community.png"))

        mod_embed = Embed(
            title="Moderation Policy",
            description="**1.** Please ping individual online staff members if there is an issue. Only ping"
            f" {(ctx.guild.get_role(Roles.moderator)).mention} when"
            " the situation is extreme (raids, spam, etc.).\n"
            "**2.** Staff members support this community in their own free time, when they can."
            " We cannot always respond right away, but will refer the user to another staff member who is"
            " available to help.\n"
            "**3.**Moderation actions may be taken at the discretion of the moderation team, for both"
            " explicit rule violations and in cases where a user's behaviour violates"
            " the spirit of the rules.",
            color=Colors.green,
        ).set_thumbnail(file=File("venkatesh/assets/icon_moderator.png"))

        await ctx.send(embeds=[rules_embed, community_embed, mod_embed])


def setup(bot: commands.Bot) -> None:
    """Loads the Rules cog."""
    bot.add_cog(Rules(bot))
