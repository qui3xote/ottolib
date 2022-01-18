from pyparsing import CaselessKeyword, Or

# Keywords
WHEN = CaselessKeyword('WHEN')
IF = CaselessKeyword('IF')
THEN = CaselessKeyword('THEN')
ELSE = CaselessKeyword('ELSE')
FROM = CaselessKeyword('FROM')
WITH = CaselessKeyword('WITH')
IS = CaselessKeyword('IS')
FOR = CaselessKeyword('FOR')
TRUE = CaselessKeyword('TRUE')
CHANGES = CaselessKeyword('CHANGES')
AND = CaselessKeyword('AND')
OR = CaselessKeyword('OR')
NOT = CaselessKeyword('NOT')
END = CaselessKeyword('END')
CASE = CaselessKeyword('CASE')
TO = CaselessKeyword('TO')
ON = CaselessKeyword('ON')
OFF = CaselessKeyword('OFF')

# Time
HOUR = Or(map(CaselessKeyword, ["HOUR", "HOURS"]))
MINUTE = Or(map(CaselessKeyword, ["MINUTE", "MINUTES", "MIN"]))
SECOND = Or(map(CaselessKeyword, ["SECOND", "SECONDS", "SEC"]))
SUNRISE = CaselessKeyword('SUNRISE')
SUNSET = CaselessKeyword('SUNSET')
BEFORE = CaselessKeyword('BEFORE')
AFTER = CaselessKeyword('AFTER')
