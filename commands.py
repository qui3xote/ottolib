import sys
from pyparsing import *
from ottolib.vocab import *
#from utils import add_subclasses_parseres_to_scope

class BaseCommand(BaseVocab):
    _kwd = None

    def __str__(self):
        return f"command(values)"

    def run(self):
        return print(str(self))


class Set(BaseCommand):
    _kwd = CaselessKeyword("SET")
    _parser = _kwd + Entity.parser()("_entity") + (CaselessKeyword("TO") | "=") + (Var.parser() | Numeric.parser() | StringValue.parser())("_newvalue")

    def __str__(self):
        return f"state.set({self._entity.name},{self._newvalue})"

    def eval(self):
        return [{'opfunc': 'set_state', 'args': [self._entity.name], 'kwargs': {'value': self._newvalue.value}}]

class Wait(BaseCommand):
    _kwd = CaselessKeyword("WAIT")
    _parser = _kwd + (TimeStamp.parser() | RelativeTime.parser())("_time")

    def __str__(self):
        return f"task.sleep({self._time.as_seconds})"

    def eval(self):
        return [{'opfunc': 'sleep', 'args': self._time.as_seconds}]

class Turn(BaseCommand):
    _kwd = CaselessKeyword("TURN")
    _parser = _kwd + (CaselessKeyword("ON") | CaselessKeyword("OFF"))('_newstate') + Entity.parser()("_entity")

    def eval(self):
        domain = self._entity.domain
        servicename = 'turn_'+self._newstate.lower()
        entity_id = self._entity.name
        operation = {'opfunc':'service_call', 'args':[domain, servicename], 'kwargs': {'entity_id': entity_id}}
        return [operation]
