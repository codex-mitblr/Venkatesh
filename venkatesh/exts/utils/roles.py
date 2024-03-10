from datetime import datetime

from disnake import (
    ApplicationCommandInteraction,
    ButtonStyle,
    Embed,
    Guild,
    MessageInteraction,
    ModalInteraction,
    Role,
    SelectOption,
    TextInputStyle,
)
from disnake.ext import commands
from disnake.ui import Button, StringSelect, TextInput
from loguru import logger

from ...constants import Channels, Colors, Departments, Roles


class DepartmentRoles(commands.Cog):
    """Roles assigned per department."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.dept_list: list[Role] | None = None

    async def get_dept_roles(self, guild: Guild) -> list:
        """Get each role listed under DepartmentRoles."""
        if self.dept_list is None:
            await self.bot.wait_until_ready()
            self.dept_list = [
                guild.get_role(Departments.__dict__[role])
                for role in dir(Departments)
                if not callable(getattr(Departments, role)) and not role.startswith("_")
            ]

            if self.dept_list is None:
                logger.error("Failed to get department roles.")

        return self.dept_list

    @commands.command()
    @commands.cooldown(3, 30)
    @commands.has_any_role(Roles.moderator)
    async def roles(self, ctx: commands.Context, reg_disabled: str = None) -> None:
        """Sends the announcement message to register."""
        if reg_disabled:
            description = "Registrations are currently closed. You can proceed to join as a guest."
        else:
            description = (
                "Register to join the club, or proceed to the server as a guest!"
            )

        embed = Embed(
            title="Member Registration",
            description=description
            + f" **By proceeding, you agree to {(await self.bot.fetch_channel(Channels.rules)).mention}.**",
            color=Colors.orange,
        ).set_author(
            name="Team CodeX",
            icon_url="https://codex.mitb.club/brand_enlarged.png",
        )

        await ctx.send(
            embed=embed,
            components=[
                Button(
                    label="Register",
                    style=ButtonStyle.success,
                    disabled=(True if reg_disabled else False),
                    custom_id="reg_button",
                ),
                Button(
                    label="Join as Guest",
                    style=ButtonStyle.gray,
                    disabled=False,
                    custom_id="reg_guest",
                ),
            ],
        )

    @commands.Cog.listener()
    async def on_button_click(self, inter: MessageInteraction) -> None:
        """Handles modal interaction for registration."""
        if inter.component.custom_id not in ["reg_button", "reg_guest"]:
            return

        member = inter.guild.get_role(Roles.member)
        if member in inter.user.roles:
            return await inter.response.send_message(
                "You are already registered. Use `/departments` at any time to choose your departments!",
                ephemeral=True,
            )

        guest = inter.guild.get_role(Roles.guest)
        if guest in inter.user.roles:
            await inter.user.remove_roles(guest)
            if inter.component.custom_id == "reg_guest":
                return await inter.response.send_message(
                    "Your guest role has been removed.", ephemeral=True
                )

        if inter.component.custom_id == "reg_guest":
            await inter.user.add_roles(guest)
            return await inter.response.send_message(
                "You have been registered as a guest!", ephemeral=True
            )

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
                    label="Registration Number (Starts with 22...)",
                    placeholder="1234567890",
                    custom_id="Registration Number",
                    style=TextInputStyle.short,
                    max_length=12,
                ),
                TextInput(
                    label="Learner's Email Address",
                    placeholder="butternaan@learner.manipal.edu",
                    custom_id="Learner's Email Address",
                    style=TextInputStyle.short,
                    max_length=50,
                ),
                TextInput(
                    label="Phone Number (For logging purposes)",
                    placeholder="1234567890",
                    custom_id="Phone Number",
                    style=TextInputStyle.short,
                    max_length=10,
                ),
            ],
        )

    @commands.Cog.listener()
    async def on_modal_submit(self, inter: ModalInteraction) -> None:
        """Handles data received from modal."""
        if inter.custom_id != "reg_modal":
            return

        await inter.user.add_roles(
            inter.guild.get_role(Roles.member), reason="Member registered"
        )

        await inter.response.send_message(
            "You have been registered. Use `/departments` at any time to choose your departments!",
            ephemeral=True,
        )

        embed = Embed(
            title=f"Member Registration ({inter.user.id})",
            color=Colors.green,
            timestamp=datetime.now(),
        ).set_thumbnail(url=inter.user.display_avatar.url)

        for reg_name, reg_no in inter.text_values.items():
            embed.add_field(name=reg_name, value=reg_no, inline=False)

        await self.bot.get_channel(Channels.memberinfo).send(embed=embed)

    @commands.slash_command()
    @commands.cooldown(1, 43200, commands.BucketType.user)
    @commands.has_any_role(Roles.member)
    async def departments(self, inter: ApplicationCommandInteraction) -> None:
        """Choose your departments within the club! Your current roles will be reset."""
        embed = Embed(
            title="Department Selection",
            description="Your current departments have been removed."
            " Please select (upto 3) departments from the following list.",
            color=Colors.blue,
            timestamp=datetime.now(),
        )

        await inter.response.send_message(
            embed=embed,
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
                            label="CXDS - Data Science",
                            value=Departments.cxds,
                            emoji="\N{INPUT SYMBOL FOR NUMBERS}",
                        ),
                    ],
                ),
            ],
            ephemeral=True,
        )

    @departments.error
    async def departments_errors(
        self,
        inter: ApplicationCommandInteraction,
        error: commands.CommandError,
    ) -> None:
        """Returns respective error for the `departments` command."""
        if isinstance(error, commands.CommandOnCooldown):
            embed = Embed(
                title="Command On Cooldown",
                description="You can change departments every 12 hours."
                " Please refrain from using the command too frequently.",
                color=Colors.orange,
                timestamp=datetime.now(),
            )
        elif isinstance(error, commands.MissingAnyRole):
            embed = Embed(
                title="Missing Permissions",
                description="This command is only open to registered CodeX members.",
                color=Colors.orange,
                timestamp=datetime.now(),
            )
        else:
            return

        await inter.response.send_message(embed=embed, ephemeral=True)

    @commands.Cog.listener()
    async def on_dropdown(self, inter: MessageInteraction) -> None:
        """Adds respective department roles to the user."""
        if inter.component.custom_id != "reg_dept_select":
            return

        dept_roles = await self.get_dept_roles(inter.guild)
        user_roles = [role for role in dept_roles if role in inter.user.roles]

        if user_roles is not None:
            await inter.user.remove_roles(*user_roles)

        selected_roles = [role for role in dept_roles if str(role.id) in inter.values]

        await inter.user.add_roles(*selected_roles)

        await inter.response.send_message(
            f"Your enrolled departments are: {' '.join([role.mention for role in selected_roles])}",
            ephemeral=True,
        )

        embed = Embed(
            title="Member Departments Changed",
            color=Colors.yellow,
            timestamp=datetime.now(),
        ).set_author(name=inter.user, icon_url=inter.user.display_avatar.url)

        embed.add_field(
            name="Old Departments",
            value=" ".join([role.mention for role in user_roles]),
            inline=False,
        )
        embed.add_field(
            name="New Departments",
            value=" ".join([role.mention for role in selected_roles]),
        )

        await self.bot.get_channel(Channels.memberinfo).send(embed=embed)


def setup(bot: commands.Bot) -> None:
    """Loads the DepartmentRoles cog."""
    bot.add_cog(DepartmentRoles(bot))
