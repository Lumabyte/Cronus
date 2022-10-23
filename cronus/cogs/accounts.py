
from discord.ext import commands
import discord
from cronus.db import Session

class Accounts(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.session = Session()

    @commands.command()
    async def auth(self, ctx: discord.ext.commands.Context):
        """
        authenticate an identity
        """
        await ctx.send('Press to increment')

    @commands.command()
    async def register(self, ctx: discord.ext.commands.Context):
        """
        register yourself for an account
        """
        await ctx.send('Press to increment')

    @commands.command()
    async def link(self, ctx: discord.ext.commands.Context):
        """
        link an identity - use some clever otp style verification
        """
        await ctx.send('Press to increment')

    async def authenticate():
        pass

    async def create_link_code():
        pass

    async def verify_link_code():
        pass

    