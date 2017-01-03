import ast
import re
from typing import Any, Generator, List, Tuple

from .keywords import ABBREVIATED_KEYWORDS, KEYWORDS
from .parser import parse


__version__ = "0.1"

SQL_RE = re.compile(
    r'(select\s.*from\s|'
    r'delete\s+from\s|'
    r'insert\s+into\s.*values\s|'
    r'update\s.*set\s)',
    re.IGNORECASE | re.DOTALL,
)
WORD_RE = re.compile(r'[\w]+')
INCORRECT_WHITESPACE_AROUND_COMMA_RE = re.compile(r'(,[\S^\n]|\s,)')
INCORRECT_WHITESPACE_AROUND_EQUALS_RE = re.compile(r'(\S=|=\S)')


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
        words = WORD_RE.findall(query.s)
        for word in words:
            if word.upper() in ABBREVIATED_KEYWORDS:
                yield(
                    query.lineno, query.col_offset,
                    "Q442 avoid abbreviated keywords, {}".format(word),
                    type(self),
                )
            if word.upper() in KEYWORDS:
                if word.upper() != word:
                    yield(
                        query.lineno, query.col_offset,
                        "Q440 keyword {} is not uppercase".format(word),
                        type(self),
                    )
            else:
                if word.lower() != word:
                    yield(
                        query.lineno, query.col_offset,
                        "Q441 name {} is not snake_case".format(word),
                        type(self),
                    )

    def _check_query_whitespace(
            self, query: ast.Str,
    ) -> Generator[Tuple[int, int, str, type], Any, None]:
        if INCORRECT_WHITESPACE_AROUND_COMMA_RE.search(query.s) is not None:
            yield(
                query.lineno, query.col_offset,
                "Q443 incorrect whitespace around comma",
                type(self),
            )
        if INCORRECT_WHITESPACE_AROUND_EQUALS_RE.search(query.s) is not None:
            yield(
                query.lineno, query.col_offset,
                "Q444 incorrect whitespace around equals",
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
