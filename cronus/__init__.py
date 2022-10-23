import logging
import asyncio
from aiohttp import web
import discord
from discord.ext.commands import Bot

TOKEN = "NzEwNzQ0NzU0Mzc1MzYwNTQ1.GKVcSF.zvO-J0GfZMNFksSWLGKJ-XmCQKcQufVfz_nuD4"

class Bottie():

    def __init__(self, loop=None, logger=None) -> None:
        # load shit from config file
        if not loop:
            loop = asyncio.get_event_loop()
        self._loop = loop
        if not logger:
            logger = logging.getLogger("bottie")
        self._logger = logger

        self.__setup_db()
        self.__setup_discord()
        self.__setup_http()
        self.__setup_ws()

    def run(self):
        asyncio.run(self.__start())

    async def __start(self) -> None:
        async with self._discord:
            await self._discord.start(TOKEN)

    def __stop(self) -> None:
        pass

    def __setup_discord(self) -> None:
        self._discord = Bot(loop=self._loop, command_prefix=discord.ext.commands.when_mentioned_or(
            '!'), intents=discord.Intents.default())

    def __setup_http(self) -> None:
        self._rest = web.Application()

    def __setup_ws(self) -> None:
        pass

    def __setup_db(self) -> None:
        pass
