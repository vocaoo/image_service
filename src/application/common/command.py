from abc import ABC

from didiator import CommandHandler as DCommandHandler, Command as DCommand


class Command[CRes](DCommand[CRes], ABC):
    pass


class CommandHandler[C: Command, CRes](DCommandHandler[C, CRes], ABC):
    pass
