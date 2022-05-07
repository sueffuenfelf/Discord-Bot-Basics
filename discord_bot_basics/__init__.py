"""Top-level package for Discord Bot Basics."""

__author__ = """Sofien Scholze"""
__email__ = 'sofien@scholze.dev'
__version__ = '0.1.0'

from .Database import Database as DB, TableColumn
from .DefaultCommands import DefaultCommandsCog
from .Roles import RolesCog, onlyAdmin, onlyOwner, onlyNonBlacklisted


class only:
    admin = onlyAdmin
    owner = onlyOwner
    nonBlacklisted = onlyNonBlacklisted


class cog:
    DefaultCommands = DefaultCommandsCog
    Roles = RolesCog


class database:
    Database = DB
    Column = TableColumn
