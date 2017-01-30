import ast
import re
from typing import Any, Generator, Iterable, List, Optional, Tuple, TypeVar

import sqlparse

from .keywords import ABBREVIATED_KEYWORDS, KEYWORDS
from .parser import parse


__version__ = '0.1'

SQL_RE = re.compile(
    r'(select\s.*from\s|'
    r'delete\s+from\s|'
    r'insert\s+into\s.*values\s|'
    r'update\s.*set\s)',
    re.IGNORECASE | re.DOTALL,
)


class Linter:
    name = 'sql'
    version = __version__

    def __init__(self, tree: Any, lines: List[str]) -> None:
        self.tree = tree
        self.lines = lines

    def run(self) -> Generator[Tuple[int, int, str, type], Any, None]:
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Str) and SQL_RE.search(node.s) is not None:
                yield from self._check_query_words(node)
                yield from self._check_query_whitespace(node)
                yield from self._check_query_linespace(node)

    def _check_query_words(
            self, query: ast.Str,
    ) -> Generator[Tuple[int, int, str, type], Any, None]:
        statements = sqlparse.parse(query.s)
        for token in _flattened_statements(statements):
            word = token.value
            if token.is_keyword:
                yield from self._check_keyword(word, query)
            elif token.ttype == sqlparse.tokens.Name:
                # Function identifiers/names are not recognised as keywords in
                # sqlparse, so this check is required. Note the only name-token
                # who's grandparent is a function is the function identifier.
                if (
                        token.within(sqlparse.sql.Function) and
                        isinstance(token.parent.parent, sqlparse.sql.Function) and
                        sqlparse.keywords.is_keyword(word)[0] == sqlparse.tokens.Token.Keyword
                ):
                    yield from self._check_keyword(word, query)
                elif not word.islower():
                    yield(
                        query.lineno, query.col_offset,
                        "Q441 name {} is not snake_case".format(word),
                        type(self),
                    )

    def _check_keyword(
            self, word: str, query: ast.Str,
    ) -> Generator[Tuple[int, int, str, type], Any, None]:
        if not word.isupper():
            yield(
                query.lineno, query.col_offset,
                "Q440 keyword {} is not uppercase".format(word),
                type(self),
            )
        if word.upper() in ABBREVIATED_KEYWORDS:
            yield(
                query.lineno, query.col_offset,
                "Q442 avoid abbreviated keywords, {}".format(word),
                type(self),
            )

    def _check_query_whitespace(
            self, query: ast.Str,
    ) -> Generator[Tuple[int, int, str, type], Any, None]:
        statements = sqlparse.parse(query.s)
        for before, token, after in _pre_post_iter(_flattened_statements(statements)):
            pre_whitespace = (before is not None and before.is_whitespace)
            post_whitespace = (after is not None and after.is_whitespace)
            post_newline = (after is None or after.ttype == sqlparse.tokens.Text.Whitespace.Newline)
            if token.ttype == sqlparse.tokens.Punctuation:
                if token.value == ',' and not post_whitespace:
                    yield(
                        query.lineno, query.col_offset,
                        'Q443 incorrect whitespace around comma',
                        type(self),
                    )
                elif token.value == ';' and not post_newline:
                    yield(
                        query.lineno, query.col_offset,
                        'Q446 missing newline after semicolon',
                        type(self),
                    )
            elif (
                    token.ttype == sqlparse.tokens.Comparison
                    and (not pre_whitespace or not post_whitespace)
            ):
                yield(
                    query.lineno, query.col_offset,
                    'Q444 incorrect whitespace around equals',
                    type(self),
                )

    def _check_query_linespace(
            self, query: ast.Str,
    ) -> Generator[Tuple[int, int, str, type], Any, None]:
        parsed = parse(query)
        if len(parsed) == 0 or parsed[0].line == parsed[-1].line:
            return
        previous = parsed[0]
        for phrase in parsed[1:]:
            if phrase.line == previous.line:
                message = "Q445 missing linespace between phrases {} and {}".format(
                    previous.phrase, phrase.phrase,
                )
                yield (query.lineno, query.col_offset, message, type(self))
            previous = phrase



def _flattened_statements(
        statements: Tuple[sqlparse.sql.Statement],
) -> Generator[sqlparse.sql.Token, Any, None]:
    for statement in statements:
        for token in statement.flatten():
            yield token


T = TypeVar('T')


def _pre_post_iter(
        iterable: Iterable[T],
) -> Generator[Tuple[Optional[T], T, Optional[T]], Any, None]:
    iterator = iter(iterable)
    before = None
    current = next(iterator)
    for after in iterator:
        yield (before, current, after)
        before = current
        current = after
    yield (before, current, None)
