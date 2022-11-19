import argparse
import asyncio
import logging
from inspect import getmembers, ismethod

from cronus.core import Cronus

"""
    discord:
        message
        leavechannel
        joinchannel
        ready

    twitch:
        message
        leavechannel
        joinchannel
        ready

    http:
        get
        post

    event
        response (as some responder object)
            - reply
"""

class Response:
    async def reply(self):
        pass

class Event:
    def __init__(self, response: Response) -> None:
        pass


class Plugin():

    def __init__(self, cronus: Cronus) -> None:
        super().__init__()
        if hasattr(self, "plugin_name"):
            name = getattr(self, "plugin_name")
        else:
            raise NoNameException()
        self.cronus = cronus
        self.logger = logging.getLogger(f'plugin.{name}')
        self._event_handlers = []
        self._task_handlers = []
        self._setup()

    # take an incoming event return a taskable for the core
    # app to start running the task
    async def on_event(self, source: any, source_name: any, event_name: any, *args: any, **kwargs: any):
        for event_handler in self._event_handlers:
            if not self._can_handle_event(event_handler, source_name, event_name):
                return
            if self._has_command_args(event_handler):
                pass
                # check if help is needed
                # try parse command for given field
                # change args for command usage
            try:
                await event_handler(self, source, *args, **kwargs)
            except Exception:
                self.logger.error(
                    "Failed to run event_handler for event {}", event_name)

    # populate _event_handlers with all handlers that have an attribute for
    # is_handler = True
    def _setup(self):
        for _, method in getmembers(self, ismethod):
            if self._is_handler(method):
                self._event_handlers.append(method)
                if self._has_command_args(method):
                    self._setup_argparser(method)

    def _setup_argparser(self, method: any):
        plugin_argparser = getattr(self, "plugin_argparser", None)
        if not plugin_argparser:
            plugin_name = getattr(self, "plugin_name")
            plugin_description = getattr(self, "plugin_description")
            plugin_argparser = argparse.ArgumentParser(
                prog=plugin_name,
                description=plugin_description
            )
            setattr(self, "plugin_argparser", plugin_argparser)
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
        handler_service_name = getattr(
            event_handler, "handler_service_name", None)
        if handler_service_name is not source_name:
            return False
        handler_event_name = getattr(
            event_handler, "handler_event_name", None)
        if handler_event_name is not event_name:
            return False
        if not asyncio.iscoroutinefunction(event_handler):
            return False
        return True


def plugin(name: str, description: str, priority: int = 0, dependencies: list[str] = None, parse_commands=False):
    def wrapper(cls):
        cls.plugin_name = name
        cls.plugin_descriptioon = description
        cls.plugin_priority = priority
        cls.plugin_dependencies = dependencies
        cls.plugin_parse_commands = parse_commands
        cls.plugin_argparser = None
        return cls
    return wrapper


def handler(service: str, event: str):
    def wrapper(function):
        function.is_handler = True
        function.handler_service_name = service
        function.handler_event_name = event
        return function
    return wrapper


def scheduler(cron: str):
    def wrapper(function):
        function.service = "scheduler"
        function.event = "scheduler"
        function.cron = cron
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