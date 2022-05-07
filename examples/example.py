from discord.ext import commands
import discord
import os

from DiscordBotBasics import only, Database as db, Cog


class MyCommands(commands.Cog):
    @commands.command(name="ping", help="Pong!", brief="Pong!")
    @only.nonBlacklisted
    async def pingCommand(self, ctx: commands.Context):
        await ctx.send("Pong!")


if __name__ == "__main__":
    # create intents to be able to see servers members
    intents = discord.Intents.default()
    intents.members = True

    # initialize bot
    bot = commands.Bot(command_prefix="!", intents=intents)

    # initialize database
    db = db.Database("./database.db")
    # add Cog's
    bot.add_cog(Cog.Roles(db))
    bot.add_cog(
        Cog.DefaultCommands(db).setDonationLink('Your donation link here')
    )
    bot.add_cog(MyCommands())

    # run bot
    bot.run(os.getenv('BOT_TOKEN'))
