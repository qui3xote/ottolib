from pyparsing import (Group, Optional, MatchFirst,
                       Suppress, ZeroOrMore, OneOrMore)
from .keywords import AUTOMATION, RESTART, WHEN
from .ottobase import OttoBase
from .datatypes import ident, Var
from .commands import Assignment
from .conditionals import IfThenElse, Case, Then
from .triggers import StateTrigger, TimeTrigger


class AutoControls(OttoBase):
    parser = Group(
        AUTOMATION
        + ident("name")
        + Optional(
            Var(fetch=False)('_trigger_var')
        )
        + Optional(
            RESTART('restart_option')
        )
    )

    @property
    def trigger_var(self):
        if hasattr(self, '_trigger_var'):
            return self._trigger_var.name
        else:
            return '@trigger'

    @property
    def restart(self):
        return hasattr(self, 'restart_option')

    def __init__(self, tokens):
        super().__init__(tokens)
        print(f"setting name to {self.name}")
        self.ctx.set_name(self.name)


class Actions(OttoBase):
    conditionals = (IfThenElse() | Case())
    parser = Group(
        OneOrMore(conditionals | Then())("clauses")
    )

    async def eval(self, interpreter):
        for clause in self.clauses:
            await clause.eval(interpreter)


class GlobalParser(OttoBase):
    parser = Group(
        ZeroOrMore(
            Assignment("external")
        )("assignments")
    )


class Trigger(OttoBase):
    parser = Group(
        Suppress(WHEN)
        + MatchFirst(
            StateTrigger.parsers()
            + TimeTrigger.parsers()
        )("_trigger_list")
    )

    @property
    def trigger_list(self):
        return [
            {"type": trigger.type, 'string': string}
            for trigger in self._trigger_list
            for string in trigger.strings
        ]


class Auto(OttoBase):
    parser = Group(
        GlobalParser()("globals")
        + AutoControls()("controls")
        + OneOrMore(
            Trigger()
        )("triggers")
        + Actions()("actions")
    )
