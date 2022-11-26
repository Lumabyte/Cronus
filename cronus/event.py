from cronus.service import Service


class Event(dict):
    def __init__(self, source: Service, name: str, *args, **kwargs) -> None:
        self._source = source
        self._name = name

    @property
    def source(self) -> Service:
        return self._source

    @property
    def source_name(self) -> str:
        return self._source.name

    @property
    def name(self) -> str:
        return self._name

    async def reply(self, *args, **kwargs) -> None:
        pass

    def get_identity(self) -> str:
        pass

