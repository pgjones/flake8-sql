import ast
import re
from typing import Any, Generator, Iterable, List, Optional, Tuple, TypeVar

from .keywords import ABBREVIATED_KEYWORDS
from .parser import Parser, parse


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
                parser = Parser(node.s)
                yield from self._check_query_words(node, parser)
                yield from self._check_query_whitespace(node, parser)
                yield from self._check_query_linespace(node, parser)

    def _check_query_words(
            self, query: ast.Str, parser: Parser,
    ) -> Generator[Tuple[int, int, str, type], Any, None]:
        for token in parser:
            word = token.value
            if token.is_keyword:
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
            elif token.is_name and not word.islower():
                yield(
                    query.lineno, query.col_offset,
                    "Q441 name {} is not snake_case".format(word),
                    type(self),
                )

    def _check_query_whitespace(
            self, query: ast.Str, parser: Parser,
    ) -> Generator[Tuple[int, int, str, type], Any, None]:
        for before, token, after in _pre_post_iter(parser):
            pre_whitespace = (before is not None and before.is_whitespace)
            post_whitespace = (after is not None and after.is_whitespace)
            post_newline = (after is None or after.is_newline)
            if token.is_punctuation:
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
                    token.is_comparison
                    and (not pre_whitespace or not post_whitespace)
            ):
                yield(
                    query.lineno, query.col_offset,
                    'Q444 incorrect whitespace around equals',
                    type(self),
                )

    def _check_query_linespace(
            self, query: ast.Str, parser: Parser,
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
