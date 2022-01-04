from pyparsing import *
from ottolib.vocab import *
from ottolib.commands import *
from ottolib.teststrings import *
from ottolib.conditions import *
from ottolib.triggers import *


class OttoScript:
    command = Or([cls.parser() for cls in BaseCommand.__subclasses__()])
    trigger = Or([cls.parser() for cls in BaseTrigger.__subclasses__()])
    condition = Or([cls.parser() for cls in BaseCondition.__subclasses__()])

    WHEN, THEN = map(CaselessKeyword, ["WHEN", "THEN"])

    when_expr = WHEN.suppress() + Group(trigger)("when")
    then_clause = THEN.suppress() + Group(OneOrMore(command))("actions")
    conditionclause = condition("conditions") + then_clause
    _parser = when_expr + OneOrMore(Group(conditionclause))("condition_clauses")

    def __init__(self, interpreter, script):
        BaseVocab.set_interpreter(interpreter)
        self.interpreter = interpreter
        self._parsobj = self.parse(script)


    @property
    def parser(self):
        return self._parser

    def parse(self, script):
        return self.parser.parse_string(script)

    @property
    def trigger(self):
        return self._parsobj.when[0]

    async def execute(self):
        await self.interpreter.log_info("Executing")
        for conditions, commands in self._parsobj.condition_clauses.as_list():
            await self.interpreter.log_info("In loop")
            await self.interpreter.log_info(f"Condtions: {type(conditions)}")
            if await conditions.eval() == True:
                await self.interpreter.log_info("Conditions true")
                for command in commands:
                    await command.eval()
            else:
                await self.interpreter.log_info(f"Condition Failed")
