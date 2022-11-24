import argparse
import asyncio
from dataclasses import dataclass
from logging import getLogger, Logger
from inspect import getmembers, ismethod

from cronus.event import Event

class Key:
    PLUGIN_NAME = "plugin_name"
    PLUGIN_DESCRIPTION = "plugin_description"
    PLUGIN_PRIORITY = "plugin_priority"
    PLUGIN_DEPENDENCIES = "plugin_dependencies"
    HANDLER_IS_HANDLER = "handler_is_handler"
    HANDLER_SERVICE_FILTER = "handler_service_filter"
    HANDLER_EVENT_FILTER = "handler_event_filter"
    AUTH_REQUIRED = "auth_required"
    AUTH_SCOPES = "auth_scopes"

@dataclass
class PluginTask:
    task: any
    scopes: list[str]


class Plugin:
    def __init__(self) -> None:
        super().__init__()
        if hasattr(self, Key.PLUGIN_NAME):
            self._name = getattr(self, Key.PLUGIN_NAME)
        if hasattr(self, Key.PLUGIN_DESCRIPTION):
            self._description = getattr(self, Key.PLUGIN_DESCRIPTION)
        self._logger = getLogger(f"plugin.{self._name}")
        self._event_handlers = []
        self._task_handlers = []
        self._argparser = None
        self._setup()

    @property
    def name(self) -> str:
        return self._name

    @property
    def logger(self) -> Logger:
        return self._logger

    # take an incoming event return a taskable for the core
    # app to start running the task
    # TODO: source_name can come from the source, event needs to be a new object
    async def on_event(self, event: Event): PluginTask
        for event_handler in self._event_handlers:
            if not self._can_handle_event(event_handler, event.source, event.name):
                return
            if self._has_command_args(event_handler):
                print(event_handler)
                # check if help is needed
                # try parse command for given field
                # change args for command usage
            #try:
            #    await event_handler(self, source, *args, **kwargs)
            #except Exception:
            #    self.logger.error("Failed to run event_handler for event %s", event_name)

    # populate _event_handlers with all handlers that have an attribute for
    # is_handler = True
    def _setup(self):
        for _, method in getmembers(self, ismethod):
            if self._is_handler(method):
                self._event_handlers.append(method)
                if self._has_command_args(method):
                    self._setup_argparser(method)

    def _setup_argparser(self, method: any):
        if not self._argparser:
            self._argparser = argparse.ArgumentParser(prog=self.name, description=self._description)
        argparser_argument = getattr(method, "argparser_argument")
        plugin_argparser.add_argument(**argparser_argument)

    def _is_handler(self, method) -> bool:
        return hasattr(method, "is_handler")

    def _has_command_args(self, event_handler) -> bool:
        if getattr(self, "plugin_parse_commands", False) and hasattr(event_handler, "argparser_argument"):
            return True
        return False

    def _get_event_handlers(self):
        for event_handler in self._event_handlers:
            return event_handler

    def _can_handle_event(self, event_handler, source_name, event_name) -> bool:
        handler_service_name = getattr(event_handler, "handler_service_name", None)
        if handler_service_name is not source_name:
            return False
        handler_event_name = getattr(event_handler, "handler_event_name", None)
        if handler_event_name is not event_name:
            return False
        if not asyncio.iscoroutinefunction(event_handler):
            return False
        return True


def plugin(name: str, description: str, priority: int = 0, dependencies: list[str] = None):
    def wrapper(cls):
        cls[Key.PLUGIN_NAME] = name
        cls[Key.PLUGIN_DESCRIPTION] = description
        cls[Key.PLUGIN_PRIORITY] = priority
        cls[Key.PLUGIN_DEPENDENCIES] = dependencies
        return cls
    return wrapper


def handler(service: str = None, event: str = None):
    def wrapper(function):
        function[Key.HANDLER_IS_HANDLER] = True
        function[Key.HANDLER_SERVICE_FILTER] = service
        function[Key.HANDLER_EVENT_FILTER] = event
        return function
    return wrapper

def authorized(requires: list[str] = None):
    def wrapper(function):
        function[Key.AUTH_REQUIRED] = True
        function[Key.AUTH_SCOPES] = requires
        return function
    return wrapper

class NoNameException(Exception):
    pass


@handler(service=None, event="message")
def command(*args):
    def wrapper(function):
        function.argparser_argument = args
        return function
    return wrapper
