from pyparsing import (Group, Optional, MatchFirst,
                       Suppress, OneOrMore)
from .keywords import AUTOMATION, RESTART, WHEN
from .ottobase import OttoBase
from .datatypes import ident, Var
from .commands import Assignment
from .conditionals import IfThenElse, Case, Then
from .triggers import StateTrigger, TimeTrigger


class AutoControls(OttoBase):
    parser = Group(AUTOMATION
                   + ident("name")
                   + Optional(Var()('_trigger_var'))
                   + Optional(RESTART('restart_option'))
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


class Actions(OttoBase):
    conditionals = (IfThenElse() | Case())
    parser = Group(OneOrMore(conditionals | Then())("clauses"))

    async def eval(self, interpreter):
        for clause in self.clauses:
            await clause.eval(interpreter)


class Auto(OttoBase):
    trigger = Suppress(WHEN) \
        + MatchFirst(StateTrigger.parsers() + TimeTrigger.parsers())

    parser = Group(AutoControls()("controls")
                   + OneOrMore(trigger)("triggers")
                   + Group(Actions())('actions'))


class GlobalParser(OttoBase):
    parser = Group(OneOrMore(Assignment("external"))("assignments"))
