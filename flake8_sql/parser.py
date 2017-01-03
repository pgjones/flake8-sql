import ast
import re
from typing import List, NamedTuple

Phrase = NamedTuple('Phrase', [('phrase', str), ('line', int)])


PHRASES_RE = re.compile(
    r'(select\s|'
    r'from\s|'
    r'delete\s+from\s|'
    r'insert\s+into\s|'
    r'values\s|'
    r'update\s|'
    r'set\s|'
    r'where\s|'
    r'\n)',
    re.IGNORECASE,
)


def parse(query: ast.Str) -> List[Phrase]:
    parsed = []
    line = 0
    for phrase in PHRASES_RE.finditer(query.s):
        if phrase.group() == '\n':
            line += 1
        else:
            parsed.append(Phrase(phrase.group().strip(), line))
    return parsed
