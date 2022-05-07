import datetime
from types import FunctionType
from discord.ext import commands
import discord
from DiscordBotBasics.Database import Database, TableColumn
import peewee
from typing import Dict, List


def onlyAdmin(func: FunctionType):
    async def wrapped(cog, ctx: commands.Context, *args, **kwargs):
        if ctx.author.id == cog.bot.owner_id:
            return await func(cog, ctx, *args, **kwargs)
        adminRole = RolesCog.getAdminRoleId(ctx.guild.id)
        if adminRole == -1:
            await ctx.send("Warning: Admin role is not set")
        author: discord.User = ctx.author
        for role in author.roles:
            if role.id == adminRole:
                return await func(cog, ctx, *args, **kwargs)
        await ctx.send("Error: You don't have rights to use this command")
    return wrapped


def onlyOwner(func: FunctionType):
    async def wrapped(rolesCog, ctx: commands.Context, *args, **kwargs):
        if ctx.author.id == ctx.guild.owner.id:
            return await func(rolesCog, ctx, *args, **kwargs)
        await ctx.send("Error: Only the servers owner can use this command")
    return wrapped


def onlyNonBlacklisted(func: FunctionType):
    async def wrapped(rolesCog, ctx: commands.Context, *args, **kwargs):
        if RolesCog.isBlacklisted(ctx.author.id):
            await ctx.send("Error: You are not allowed to use this command")
        else:
            return await func(rolesCog, ctx, *args, **kwargs)
    return wrapped


class RolesCog(commands.Cog, name="Admin"):
    def __init__(self, db: Database):
        self._db = db
        RolesCog._models: Dict[str, peewee.Model] = {}
        self.initDatabaseModels()

    def initDatabaseModels(self) -> None:
        RolesCog._models['admin'] = self._db.createModel('Admin_Role', [
            TableColumn('id', peewee.IntegerField(primary_key=True)),
            TableColumn('server_guild_id', peewee.IntegerField(unique=True)),
            TableColumn('role_id', peewee.IntegerField()),
        ])
        RolesCog._models['blacklist'] = self._db.createModel('blacklist', [
            TableColumn('id', peewee.IntegerField(primary_key=True)),
            TableColumn('server_guild_id', peewee.IntegerField()),
            TableColumn('user_id', peewee.IntegerField()),
        ])

    @staticmethod
    def isBlacklisted(userId: int) -> bool:
        try:
            blacklistModel = RolesCog.getModel('blacklist')
            blacklistModel.get(blacklistModel.user_id == userId)
            return True
        except peewee.DoesNotExist:
            return False

    @staticmethod
    def getAdminRoleId(guildId: int) -> int:
        try:
            return RolesCog.getModel('admin').get(
                server_guild_id=guildId
            ).role_id
        except peewee.DoesNotExist:
            return -1

    @staticmethod
    def getModel(modelName: str) -> peewee.Model:
        return RolesCog._models[modelName]

    @commands.command(
        name="setAdminRole",
        help="""Sets the new admin role.
            Can only be used by the server owner
        """,
        usage="<roleId>"
    )
    @onlyOwner
    async def changeAdminRole(self, ctx: commands.Context, roleId: int, *args) -> None:
        try:
            roleId = int(roleId)
        except ValueError:
            await ctx.send("Error: Role ID must be an integer")
        for role in ctx.guild.roles:
            if role.id == roleId:
                try:
                    RolesCog.getModel('admin').get(
                        server_guild_id=ctx.guild.id
                    ).delete_instance()
                except peewee.DoesNotExist:
                    pass
                RolesCog.getModel('admin').create(
                    server_guild_id=ctx.guild.id,
                    role_id=roleId
                )
                await ctx.send(f"Admin role set to '{role.name if role else roleId}'")
                return
        await ctx.send(f"Error: Role with id '{roleId}' not found")

    @commands.command(
        name="blacklist",
        help="""Adds or removes specified user id to/from blacklist.""",
        usage="<'add' or 'remove'><userId>"
    )
    @onlyAdmin
    async def blacklistUser(self, ctx: commands.Context, method: str, userId: int, *args) -> None:
        blacklistModel = RolesCog.getModel('blacklist')
        if self.isBlacklisted(userId):
            if method == "add":
                await ctx.send(f"Error: User with id '{userId}' is already blacklisted")
            elif method == "remove":
                blacklistModel.get(
                    blacklistModel.user_id == userId).delete_instance()
                await ctx.send(f"User with id '{userId}' removed from blacklist")
        else:
            if method == "add":
                blacklistModel.create(
                    server_guild_id=ctx.guild.id,
                    user_id=userId
                )
                await ctx.send(f"User with id '{userId}' blacklisted")
            elif method == "remove":
                await ctx.send(f"Error: User with id '{userId}' is not blacklisted")
        if not method in ["add", "remove"]:
            await ctx.send("Error: Method must be 'add' or 'remove'")


if __name__ == "__main__":
    import os
    intents = discord.Intents.default()
    intents.members = True
    bot = commands.Bot(command_prefix="!", intents=intents)
    db = Database('./test.db')
    rolesCog = RolesCog(bot, db)

    bot.run(os.getenv('BOT_TOKEN'))
