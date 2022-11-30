class Event:
    def __init__(self, event: str, data: any) -> None:
        self._event = event
        self._data = data

    @property
    def event(self) -> str:
        return self._event

    @property
    def data(self) -> any:
        return self._data
