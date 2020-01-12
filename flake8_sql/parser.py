from typing import Any, Generator, List, Tuple

import sqlparse

from .keywords import ROOT_KEYWORDS


class Token:

    def __init__(self, token: sqlparse.sql.Token, row: int, col: int, depth: int) -> None:
        self._token = token
        self.row = row
        self.col = col
        self.depth = depth

    @property
    def is_whitespace(self) -> bool:
        return self._token.is_whitespace

    @property
    def is_keyword(self) -> bool:
        return self._token.is_keyword

    @property
    def is_root_keyword(self) -> bool:
        if not self.is_keyword:
            return False
        value = self.value.split()[-1].upper()
        if value == "FROM" and isinstance(self._token.parent.parent, sqlparse.sql.Function):
            return False
        return value in ROOT_KEYWORDS

    @property
    def is_function_name(self) -> bool:
        # Note the only name-token who's grandparent is a function is
        # the function identifier.
        return (
            self._token.ttype == sqlparse.tokens.Name and
            self._token.within(sqlparse.sql.Function) and
            isinstance(self._token.parent.parent, sqlparse.sql.Function) and
            sqlparse.keywords.is_keyword(self._token.value)[0] == sqlparse.tokens.Token.Keyword
        )

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

    def __init__(self, sql: str, initial_offset: int) -> None:
        self._initial_offset = initial_offset
        self._tokens = []  # type: Tuple[sqlparse.sql.Token, int]
        depth = 0
        for statement in sqlparse.parse(sql):
            for token in statement.tokens:
                if token.is_group:
                    self._tokens.extend(_flatten_group(token, depth))
                else:
                    self._tokens.append((token, depth))

    def __iter__(self) -> Generator[Token, Any, None]:
        row = 0
        col = self._initial_offset
        for sql_token, depth in self._tokens:
            token = Token(sql_token, row, col, depth)
            yield token
            if token.is_newline:
                row += 1
                col = 0
            else:
                col += len(token.value)


def _flatten_group(token: sqlparse.sql.Token, depth: int = 0) -> List[sqlparse.sql.Token]:
    tokens = []
    for item in token.tokens:
        if item.ttype == sqlparse.tokens.DML:
            depth += 1
        if item.is_group:
            tokens.extend(_flatten_group(item, depth))
        else:
            tokens.append((item, depth))
    return tokens
