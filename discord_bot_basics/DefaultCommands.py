import datetime
from discord.ext import commands
import peewee
from typing import List

from DiscordBotBasics.Database import Database, TableColumn
from DiscordBotBasics.Roles import onlyNonBlacklisted


class DefaultCommandsCog(commands.Cog, name="Extra"):
    def __init__(self, db: Database):
        self._db = db
        self.feedbackModel = self.createFeedbackModel()
        self.bugModel = self.createBugModel()
        self.donationLink = "EMPTY"

    def setDonationLink(self, donationLink):
        self.donationLink = donationLink
        return self

    def createFeedbackModel(self):
        return self._db.createModel('feedback', [
            TableColumn('id', peewee.IntegerField(primary_key=True)),
            TableColumn('server_guild_id', peewee.IntegerField()),
            TableColumn('created_at', peewee.DateTimeField(
                default=datetime.datetime.now)),
            TableColumn('updated_at', peewee.DateTimeField(
                default=datetime.datetime.now)),
            TableColumn('user_id', peewee.IntegerField(unique=True)),
            TableColumn('message', peewee.TextField()),
        ])

    def createBugModel(self):
        return self._db.createModel('bug', [
            TableColumn('id', peewee.IntegerField(primary_key=True)),
            TableColumn('server_guild_id', peewee.IntegerField()),
            TableColumn('created_at', peewee.DateTimeField(
                default=datetime.datetime.now)),
            TableColumn('user_id', peewee.IntegerField()),
            TableColumn('message', peewee.TextField()),
        ])

    @commands.command(
        name="feedback",
        help="""Give me Feedback on this bot 😊
            Recalling will update past feedback
        """,
        brief="""Give me Feedback on this bot 😊""",
        usage="<message>"
    )
    @onlyNonBlacklisted
    async def feedback(self, ctx: commands.Context, *message: List[str]) -> None:
        try:
            feedback = self.feedbackModel.get(user_id=ctx.author.id)
            feedback.message = " ".join(message)
            feedback.updated_at = datetime.datetime.now()
            feedback.save()
            msg = f"{ctx.author.mention}, your feedback has been updated 🤙🏽"
        except peewee.DoesNotExist:
            self.feedbackModel.create(
                server_guild_id=ctx.guild.id,
                user_id=ctx.author.id,
                message=" ".join(message)
            )
            msg = f"{ctx.author.mention}, thank you for your feedback 🙏🏽"
        await ctx.send(msg)

    @commands.command(
        name="bug",
        help="""Inform me about bugs you have found 🙏🏽""",
        usage="<message>"
    )
    @onlyNonBlacklisted
    async def bug(self, ctx: commands.Context, *message: List[str]) -> None:
        self.bugModel.create(
            server_guild_id=ctx.guild.id,
            user_id=ctx.author.id,
            message=" ".join(message)
        )
        msg = f"Thank you for your support {ctx.author.mention}. I appreciate it 🙏🏽"
        await ctx.send(msg)

    @commands.command(
        name="donate",
        help="""I like coffee and you? 😊""",
        usage=""
    )
    async def donate(self, ctx: commands.Context) -> None:
        await ctx.send(f"If you want to support me, you can donate to my paypal account 😊: {self.donationLink}")
