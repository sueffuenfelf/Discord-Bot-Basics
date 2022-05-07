# discord-bot-basics

[![image](https://img.shields.io/pypi/v/discord-bot-basics.svg)](https://pypi.python.org/pypi/discord-bot-basics)

[![image](https://img.shields.io/conda/vn/conda-forge/discord-bot-basics.svg)](https://anaconda.org/conda-forge/discord-bot-basics)

**This package contains some features that can be used a the bases for any discord bot**

- Documentation: <https://sueffuenfelf.github.io/discord-bot-basics>

## Features

- 2 different `Cog`'s to extend the functionality of your discord bot
    - `Roles` which grants you access to the decorators `onlyAdmin`, `onlyOwner` and `nonBlacklisted`
    - `DefaultCommands` which adds the commands `feedback` and `bug` and `donate`
- `Database` class to easily access a local SQLite database file

## Installation

currently working on a pip installation.
The only option for now is to clone this repository and copy the `discord_bot_basics` folder to the folder of your project.

# Usage

## Roles feature

1. Create your own Cog class and add the commmands as you need it

```python
from discord.ext import commands

# imports
from DiscordBotBasics import only

class MyOwnCommands(commands.Cog):
    @commands.command()
    @only.nonBlacklisted
    async def onlyForNonBlacklistedUsers(self, ctx: commands.Context):
        # do some magic...
        await ctx.send('Successfully executed')

    @commands.command()
    @only.admin
    async def onlyForUsersThatHaveTheAdminRole(self, ctx: commands.Context):
        # do some magic...
        await ctx.send('Successfully executed')

    @commands.command()
    @only.owner
    async def onlyForTheOwnerOfTheDiscordServer(self, ctx: commands.Context):
        # do some magic...
        await ctx.send('Successfully executed')
```

2. create a _Database_ instance and add the _Cog_'s to your bot

```python
from discord.ext import commands
import discord
import os

# imports
from DiscordBotBasics import Database as db, Cog

# The Roles Cog needs member access to the server
intents = discord.Intents.default()
intents.members = True

# initialize the bot
myDiscordBot = commands.Bot(command_prefix="!", intents=intents)

# create database instance for the Roles Cog
myDb = db.Database('/path/to/where/the/database/file/should/be/saved.db')

# add the Cog's
myDiscordBot.add_cog(Cog.Roles(myDb))
myDiscordBot.add_cog(MyOwnCommands())

# run the bot
myDiscordBot.run(os.getenv('BOT_TOKEN'))
```

## Default Commands

Just add the Cog to your discord bot

```python
from discord.ext import commands
import discord

# imports
from DiscordBotBasics import Database as db, Cog

# initialize own bot
myDiscordBot = commands.Bot(command_prefix="!", intents=intents)

# create database instance for the DefaultCommands Cog
myDb = db.Database('/path/to/where/the/database/file/should/be/saved.db')

# add DefaultCommands Cog to the bot
myDiscordBot.add_cog(Cog.DefaultCommands(myDb))

# run the bot
myDiscordBot.run(os.getenv('BOT_TOKEN'))
```

## Database feature

This feature is based on the [peewee](https://github.com/coleifer/peewee) library (shout out to them for their great work), but added the functionality to dynamically create table models.

```python
from discord.ext import commands
import discord
import os

# imports
from DiscordBotBasics import Database as db
import peewee

# custom Cog class
class CustomDatabaseAccessClass(commands.Cog):
    def __init__(self, db: db.Database):
        self._db: db.Database = db
        
        # a dict where all custom models will be saved in
        self._models = dict()

        # initialize custom models
        self._initCustomModel()

    def _initCustomModel(self):
        # the function 'createModel' creates a new object of type 'peewee.Model'
        # to learn more about how to work with this object see the documentation
        # of peewee
        self._models['MyModel'] = self._db.createModel('my_model', [
            db.Column('id', peewee.IntegerField(primary_key=True)),
            db.Column('integer_field', peewee.IntegerField(unique=True)),
            db.Column('text_field', peewee.TextField()),
        ])

```

## Credits

This package was created with [Cookiecutter](https://github.com/cookiecutter/cookiecutter) and the [giswqs/pypackage](https://github.com/giswqs/pypackage) project template.

## License

Look up the LICENSE file at the root of this repository
