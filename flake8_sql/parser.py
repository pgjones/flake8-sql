import ast
import re
from typing import Any, Generator, List, NamedTuple

import sqlparse


Phrase = NamedTuple('Phrase', [('phrase', str), ('line', int)])


PHRASES_RE = re.compile(
    r'(select\s|'
    r'from\s|'
    r'delete\s+from\s|'
    r'insert\s+into\s|'
    r'values\s|'
    r'returning\s'
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


class Token:

    def __init__(self, token: sqlparse.sql.Token) -> None:
        self._token = token

    @property
    def is_whitespace(self) -> bool:
        return self._token.is_whitespace

    @property
    def is_keyword(self) -> bool:
        simple_keyword = self._token.is_keyword
        # Function identifiers/names are not recognised as keywords in
        # sqlparse, so this check is required. Note the only name-token
        # who's grandparent is a function is the function identifier.
        function_keyword = (
            self._token.ttype == sqlparse.tokens.Name and
            self._token.within(sqlparse.sql.Function) and
            isinstance(self._token.parent.parent, sqlparse.sql.Function) and
            sqlparse.keywords.is_keyword(self._token.value)[0] == sqlparse.tokens.Token.Keyword
        )
        return simple_keyword or function_keyword

    @property
    def is_name(self) -> bool:
        return self._token.ttype == sqlparse.tokens.Name and not self.is_keyword

    @property
    def is_punctuation(self) -> bool:
        return self._token.ttype == sqlparse.tokens.Punctuation

    @property
    def is_comparison(self) -> bool:
        return self._token.ttype == sqlparse.tokens.Comparison

    @property
    def is_newline(self) -> bool:
        return self._token.ttype == sqlparse.tokens.Text.Whitespace.Newline

    @property
    def value(self) -> str:
        return self._token.value


class Parser:

    def __init__(self, sql: str) -> None:
        self.sql = sql

    def __iter__(self) -> Generator[Token, Any, None]:
        statements = sqlparse.parse(self.sql)
        for statement in statements:
            for token in statement.flatten():
                yield Token(token)
