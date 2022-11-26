from cronus.service import Service


class Event(dict):
    def __init__(self, source: Service, name: str, data: any) -> None:
        self._source = source
        self._name = name
        self._data = data

    @property
    def source(self) -> Service:
        return self._source

    @property
    def name(self) -> str:
        return self._name

    @property
    def data(self) -> any:
        return self._data

    async def reply(self, *args, **kwargs) -> None:
        pass

    def get_identity(self) -> str:
        pass
