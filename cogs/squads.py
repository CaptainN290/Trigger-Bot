import discord
from discord import app_commands
from discord.ext import commands
import aiosqlite
from config import DB_NAME

COLOR = 0x1abc9c


class Squads(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="squadcreate", description="Create a squad")
    async def squadcreate(self, interaction: discord.Interaction, name: str):

        user_id = interaction.user.id

        async with aiosqlite.connect(DB_NAME) as db:
            cursor = await db.execute(
                "SELECT * FROM squad_members WHERE user_id=?",
                (user_id,)
            )

            if await cursor.fetchone():
                await interaction.response.send_message(
                    "You are already in a squad.",
                    ephemeral=True
                )
                return

            await db.execute(
                "INSERT INTO squads (name, leader_id) VALUES (?,?)",
                (name, user_id)
            )

            cursor = await db.execute(
                "SELECT squad_id FROM squads WHERE leader_id=?",
                (user_id,)
            )

            squad_id = (await cursor.fetchone())[0]

            await db.execute(
                "INSERT INTO squad_members (squad_id, user_id, role) VALUES (?,?,?)",
                (squad_id, user_id, "Leader")
            )

            await db.commit()

        embed = discord.Embed(
            title="🛡 Squad Created",
            description=f"Squad **{name}** has been created.",
            color=COLOR
        )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="squadinvite", description="Invite a player to your squad")
    async def squadinvite(self, interaction: discord.Interaction, member: discord.Member):

        inviter = interaction.user.id
        target = member.id

        async with aiosqlite.connect(DB_NAME) as db:
            cursor = await db.execute(
                "SELECT squad_id, role FROM squad_members WHERE user_id=?",
                (inviter,)
            )
            inviter_data = await cursor.fetchone()

            if not inviter_data or inviter_data[1] != "Leader":
                await interaction.response.send_message(
                    "Only squad leaders can invite players.",
                    ephemeral=True
                )
                return

            squad_id = inviter_data[0]

            cursor = await db.execute(
                "SELECT 1 FROM squad_members WHERE user_id=?",
                (target,)
            )

            if await cursor.fetchone():
                await interaction.response.send_message(
                    "That player is already in a squad.",
                    ephemeral=True
                )
                return

            cursor = await db.execute(
                "SELECT COUNT(*) FROM squad_members WHERE squad_id=?",
                (squad_id,)
            )
            count = (await cursor.fetchone())[0]

            if count >= 5:
                await interaction.response.send_message(
                    "Squad is full.",
                    ephemeral=True
                )
                return

            await db.execute(
                "INSERT INTO squad_members (squad_id, user_id, role) VALUES (?,?,?)",
                (squad_id, target, "Member")
            )

            await db.commit()

        await interaction.response.send_message(
            embed=discord.Embed(
                title="📨 Squad Update",
                description=f"{member.mention} joined your squad.",
                color=COLOR
            )
        )

    @app_commands.command(name="squadinfo", description="View squad info")
    async def squadinfo(self, interaction: discord.Interaction):

        user_id = interaction.user.id

        async with aiosqlite.connect(DB_NAME) as db:
            cursor = await db.execute(
                "SELECT squad_id FROM squad_members WHERE user_id=?",
                (user_id,)
            )

            squad = await cursor.fetchone()

            if not squad:
                await interaction.response.send_message(
                    "You are not in a squad.",
                    ephemeral=True
                )
                return

            squad_id = squad[0]

            cursor = await db.execute(
                "SELECT name, division, elo FROM squads WHERE squad_id=?",
                (squad_id,)
            )

            name, division, elo = await cursor.fetchone()

            cursor = await db.execute(
                "SELECT user_id, role FROM squad_members WHERE squad_id=?",
                (squad_id,)
            )

            members = await cursor.fetchall()

        member_list = ""

        for uid, role in members:
            user = await self.bot.fetch_user(uid)
            member_list += f"{user.name} — {role}\n"

        embed = discord.Embed(
            title=f"🛡 Squad: {name}",
            color=COLOR
        )

        embed.add_field(name="Division", value=division)
        embed.add_field(name="ELO", value=elo)
        embed.add_field(name="Members", value=member_list, inline=False)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="squadleave", description="Leave your squad")
    async def squadleave(self, interaction: discord.Interaction):

        user_id = interaction.user.id

        async with aiosqlite.connect(DB_NAME) as db:
            await db.execute(
                "DELETE FROM squad_members WHERE user_id=?",
                (user_id,)
            )
            await db.commit()

        await interaction.response.send_message(
            embed=discord.Embed(
                title="🚪 Left Squad",
                color=COLOR
            )
        )


async def setup(bot):
    await bot.add_cog(Squads(bot))
