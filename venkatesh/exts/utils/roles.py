from datetime import datetime

from disnake import (
    ButtonStyle,
    Embed,
    MessageInteraction,
    ModalInteraction,
    SelectOption,
    TextInputStyle,
)
from disnake.ext import commands
from disnake.ui import Button, StringSelect, TextInput

from ...constants import Channels, Departments, Roles


class DepartmentRoles(commands.Cog):
    """Roles assigned per department."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 30)
    @commands.has_any_role(Roles.moderator)
    async def roles(self, ctx: commands.Context) -> None:
        """Sends the announcement message to register."""
        await ctx.send(
            "Register to get a role!",
            components=[
                Button(
                    label="Register", style=ButtonStyle.success, custom_id="reg_button"
                ),
                Button(
                    label="Join as Guest", style=ButtonStyle.gray, custom_id="reg_guest"
                ),
            ],
        )

    @commands.Cog.listener()
    async def on_button_click(self, inter: MessageInteraction) -> None:
        """Handles modal interaction for registration."""
        if inter.component.custom_id == "reg_guest":
            guest = inter.guild.get_role(Roles.guest)
            if guest in inter.user.roles:
                await inter.user.remove_roles(
                    guest, reason="Member removed from guest list"
                )
                return await inter.response.send_message(
                    "Your guest role has been removed.", ephemeral=True
                )
            else:
                await inter.user.add_roles(guest, reason="Member joined as guest")
                return await inter.response.send_message(
                    "You have joined as a guest.", ephemeral=True
                )

        if inter.component.custom_id != "reg_button":
            return

        await inter.response.send_modal(
            title="Member Registration",
            custom_id="reg_modal",
            components=[
                TextInput(
                    label="Full Name",
                    placeholder="The Great Rochak Saini",
                    custom_id="Full Name",
                    style=TextInputStyle.short,
                    max_length=50,
                ),
                TextInput(
                    label="Registration Number",
                    placeholder="1234567890",
                    custom_id="Registration Number",
                    style=TextInputStyle.short,
                    max_length=12,
                ),
            ],
        )

    @commands.Cog.listener()
    async def on_modal_submit(self, inter: ModalInteraction) -> None:
        """Handles data received from modal."""
        if inter.custom_id != "reg_modal":
            return

        embed = Embed(
            title=f"Member Registration ({inter.user.id})",
            timestamp=datetime.now(),
        ).set_thumbnail(url=inter.user.display_avatar.url)

        for reg_name, reg_no in inter.text_values.items():
            embed.add_field(name=reg_name, value=reg_no, inline=False)

        await self.bot.get_channel(Channels.memberlog).send(embed=embed)

        await inter.response.send_message(
            "Choose your departments. (upto 3)",
            components=[
                StringSelect(
                    custom_id="reg_dept_select",
                    min_values=1,
                    max_values=3,
                    options=[
                        SelectOption(
                            label="CXSD - Software Development",
                            value=Departments.cxsd,
                            emoji="\N{PERSONAL COMPUTER}",
                        ),
                        SelectOption(
                            label="CXGD - Game Development",
                            value=Departments.cxgd,
                            emoji="\N{VIDEO GAME}",
                        ),
                        SelectOption(
                            label="CXOS - Open-Source Development",
                            value=Departments.cxos,
                            emoji="\N{DESKTOP COMPUTER}",
                        ),
                        SelectOption(
                            label="CXCP - Competitive Programming",
                            value=Departments.cxcp,
                            emoji="\N{CHEQUERED FLAG}",
                        ),
                        SelectOption(
                            label="CXIT - Information Technology",
                            value=Departments.cxit,
                            emoji="\N{CLOUD}",
                        ),
                        SelectOption(
                            label="CXAD - App Development",
                            value=Departments.cxad,
                            emoji="\N{MOBILE PHONE}",
                        ),
                        SelectOption(
                            label="CXNAT - New Age Technologies",
                            value=Departments.cxnat,
                            emoji="\N{COIN}",
                        ),
                        SelectOption(
                            label="CXDS - Data Science",
                            value=Departments.cxds,
                            emoji="\N{INPUT SYMBOL FOR NUMBERS}",
                        ),
                    ],
                ),
            ],
            ephemeral=True,
        )

    @commands.Cog.listener()
    async def on_dropdown(self, inter: MessageInteraction) -> None:
        """Adds respective department roles to user."""
        roles = list(inter.guild.get_role(int(role_id)) for role_id in inter.values)
        await inter.user.add_roles(*roles, reason="Member registered")
        await inter.response.send_message(
            f"You have been enrolled in the following departments: {role for role in roles}",
            ephemeral=True,
        )


def setup(bot: commands.Bot) -> None:
    """Loads the DepartmentRoles cog."""
    bot.add_cog(DepartmentRoles(bot))
