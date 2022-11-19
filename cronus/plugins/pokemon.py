import asyncio
import aiohttp

from cronus.plugin import Plugin, command, plugin


@plugin(name="pokemon", description="Get information about different pokemon")
class Pokemon(Plugin):

    @command([
        ('-s', '--stats'),
        ('-m', '--moves'),
        ('-a', '--abilities'),
        ('-f', '--forms'),
    ])
    async def get_pokemon(self, command_args, message):
        async with aiohttp.ClientSession() as session:
            pokemon_url = 'https://pokeapi.co/api/v2/pokemon/151'
            async with session.get(pokemon_url) as resp:
                pokemon = await resp.json()
                await message.reply(self._describe_pokemon(pokemon, command_args))

    def _describe_pokemon(self, pokemon, command_args) -> str:
        message = f'${pokemon["name"]}: '
        if command_args.stats:
            message += f' weights in at about ${pokemon["weight"]} and is roughly ${pokemon["height"]}ft tall. '
        return message


if __name__ == "__main__":
    test = Pokemon(None)
    # print(dir(test))
    # print(dir(test._event_handlers))
    x = test.handler_s1_e1("source", "pokemon whois mew")
    asyncio.run(x)
    y = test.handler_s1_e1("source", "pokemon --help")
    asyncio.run(y)
