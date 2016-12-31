import ast
import re

from flake8_sql import Linter

TEST_CASE = """
query = \"""select clmn
              FROM tbl\"""  # Q440
query = text(\"""SELECT clmn
                   FROM tbl\""")
query = "SELECT tableColumn FROM tbl"  # Q441
"""

def test_expected_errors() -> None:
    expected = set()
    lines = TEST_CASE.splitlines()
    for lineno, line in enumerate(lines):
        match = re.search(r'# (.*)$', line.strip('\n'))
        if match:
            for error_code in match.group(1).split():
                expected.add((lineno + 1, error_code))
    checker = Linter(ast.parse(TEST_CASE), lines)
    codes = set()
    for lineno, _, message, _ in checker.run():
        code, _ = message.split(' ', 1)
        codes.add((lineno, code))
    assert codes == expected
