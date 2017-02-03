import ast
import re
from typing import Any, Generator, Iterable, List, Optional, Tuple, TypeVar

from .keywords import ABBREVIATED_KEYWORDS
from .parser import Parser


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
                initial_offset = _get_initial_offset(node, self.lines)
                parser = Parser(node.s, initial_offset)
                yield from self._check_query_words(node, parser)
                yield from self._check_query_whitespace(node, parser)
                yield from self._check_query_alignment(node, parser)

    def _check_query_words(
            self, query: ast.Str, parser: Parser,
    ) -> Generator[Tuple[int, int, str, type], Any, None]:
        for token in parser:
            word = token.value
            if token.is_keyword or token.is_function_name:
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
            elif token.is_name and (not word.islower() or word.endswith('_')):
                yield(
                    query.lineno, query.col_offset,
                    "Q441 name {} is not valid, must be snake_case, and cannot "
                    "end with `_`".format(word),
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

    def _check_query_alignment(
            self, query: ast.Str, parser: Parser,
    ) -> Generator[Tuple[int, int, str, type], Any, None]:
        keywords = [
            token for token in parser
            if token.is_keyword and token.value not in {'INSERT', 'ON'}
        ]
        if keywords[0].row == keywords[-1].row:
            return

        for before, keyword, _ in _pre_post_iter(keywords):
            if before is not None and keyword.value != "SELECT":
                if before.row == keyword.row:
                    message = "Q445 missing linespace between keywords {} and {}".format(
                        before.value, keyword.value,
                    )
                    yield (query.lineno, query.col_offset, message, type(self))
                if before.col + len(before.value) != keyword.col + len(keyword.value):
                    message = "Q447 keywords {} and {} are not right aligned".format(
                        before.value, keyword.value,
                    )
                    yield (query.lineno, query.col_offset, message, type(self))


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


def _get_initial_offset(query: ast.Str, physical_lines: List[str]) -> int:
    logical_lines = query.s.splitlines()
    first_physical_line = physical_lines[query.lineno - len(logical_lines)]
    return first_physical_line.find(logical_lines[0])
