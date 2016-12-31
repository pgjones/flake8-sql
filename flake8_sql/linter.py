import ast
import re
from typing import Any, Generator, List, Tuple

from .keywords import ABBREVIATED_KEYWORDS, KEYWORDS


__version__ = "0.1"

SQL_RE = re.compile(
    r'(select\s.*from\s|' \
    r'delete\s+from\s|' \
    r'insert\s+into\s.*values\s|' \
    r'update\s.*set\s)',
    re.IGNORECASE | re.DOTALL,
)
WORD_RE = re.compile(r'[\w]+')


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
