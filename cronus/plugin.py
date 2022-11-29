import argparse
import asyncio
from typing import (
    Any,
    AsyncIterator,
    Callable,
    Coroutine,
    Dict,
    Generator,
    List,
    Optional,
    Sequence,
    TYPE_CHECKING,
    Tuple,
    Type,
    TypeVar,
    Union,
)

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
    HANDLER_COMMAND_ARGS = "handler_command_args"


@dataclass
class PluginTask:
    handler: Callable[..., Coroutine]
    scopes: list[str]


class Plugin:
    def __init__(self) -> None:
        super().__init__()
        if hasattr(self, Key.PLUGIN_NAME):
            self._name = getattr(self, Key.PLUGIN_NAME)
        if hasattr(self, Key.PLUGIN_DESCRIPTION):
            self._description = getattr(self, Key.PLUGIN_DESCRIPTION)
        if hasattr(self, Key.AUTH_SCOPES):
            self._auth_scopes = getattr(self, Key.AUTH_SCOPES)

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

    @property
    def auth_scopes(self) -> str:
        return self._auth_scopes

    def on_event(self, event: Event):
        handlers = []
        for event_handler in self._event_handlers:
            if not self._can_handle_event(event_handler, event.source.name, event.name):
                continue
            if self._has_command_args(event_handler):
                message = event.data["message"]
                if not message:
                    continue
            print(f"appending new event handler {event_handler.__name__}")
            handlers.append(event_handler(event))
        return handlers

    def _setup(self):
        for _, method in getmembers(self, ismethod):
            if self._is_handler(method):
                self._event_handlers.append(method)
                self.logger.debug("registered handler %s", method.__name__)
                if self._has_command_args(method):
                    self._setup_argparser(method)

    def _setup_argparser(self, method: any):
        if not self._argparser:
            self._argparser = argparse.ArgumentParser(prog=self.name, description=self._description)
        args = getattr(method, Key.HANDLER_COMMAND_ARGS)
        for arg in args:
            self._argparser.add_argument(arg)

    def _is_handler(self, event_handler) -> bool:
        return hasattr(event_handler, Key.HANDLER_IS_HANDLER)

    def _has_command_args(self, event_handler) -> bool:
        return hasattr(event_handler, Key.HANDLER_COMMAND_ARGS)

    def _get_event_handlers(self):
        for event_handler in self._event_handlers:
            return event_handler

    def _can_handle_event(self, event_handler, source_name, event_name) -> bool:
        handler_service_name = getattr(event_handler, Key.HANDLER_SERVICE_FILTER, None)
        if handler_service_name is not source_name:
            self.logger.info(
                "%s: %s handler_service_name does not match %s",
                event_handler.__name__,
                handler_service_name,
                source_name,
            )
            return False
        handler_event_name = getattr(event_handler, Key.HANDLER_EVENT_FILTER, None)
        if handler_event_name is not event_name:
            self.logger.info(
                "%s: %s handler_event_name does not match %s", event_handler.__name__, handler_event_name, event_name
            )
            return False
        if not asyncio.iscoroutinefunction(event_handler):
            self.logger.info("%s is not a coroutine", event_handler.__name__)
            return False
        return True


def plugin(name: str, description: str, priority: int = 0, dependencies: list[str] = None):
    def wrapper(function):
        setattr(function, Key.PLUGIN_NAME, name)
        setattr(function, Key.PLUGIN_DESCRIPTION, description)
        setattr(function, Key.PLUGIN_PRIORITY, priority)
        setattr(function, Key.PLUGIN_DEPENDENCIES, dependencies)
        return function

    return wrapper


def handler(service: str = None, event: str = None):
    def wrapper(function):
        setattr(function, Key.HANDLER_IS_HANDLER, True)
        setattr(function, Key.HANDLER_SERVICE_FILTER, service)
        setattr(function, Key.HANDLER_EVENT_FILTER, event)
        # priority
        return function

    return wrapper


def authorized(required_scopes: list[str] = None):
    def wrapper(function):
        setattr(function, Key.HANDLER_IS_HANDLER, True)
        setattr(function, Key.HANDLER_SERVICE_FILTER, required_scopes)
        return function

    return wrapper


def command(commands):
    def wrapper(function):
        setattr(function, Key.HANDLER_COMMAND_ARGS, commands)
        return function

    return wrapper


class NoNameException(Exception):
    pass
