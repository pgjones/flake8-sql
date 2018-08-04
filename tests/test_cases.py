import ast
import glob
import os
import re

import pytest

from flake8_sql import Linter


ERROR_RX = re.compile("# ((Q[0-9]{3} ?)+) ?.*$")


def _extract_expected_errors(lines):
    expected = set()
    for lineno, line in enumerate(lines):
        match = ERROR_RX.search(line)
        if match is not None:
            for error_code in match.group(1).split():
                expected.add((lineno + 1, error_code))
    return expected


def _load_test_cases():
    base_path = os.path.dirname(__file__)
    test_cases = []
    test_case_path = os.path.join(base_path, 'test_cases')
    wildcard_path = os.path.join(test_case_path, '*.py')

    for filename in glob.glob(wildcard_path):
        print(filename)
        if filename.endswith('fstring.py') and not hasattr(ast, 'JoinedStr'):
            continue
        fullpath = os.path.join(test_case_path, filename)
        with open(fullpath) as file_:
            data = file_.read()
        lines = data.splitlines()
        codes = _extract_expected_errors(lines)
        tree = ast.parse(data)
        test_cases.append((tree, lines, codes))

    return test_cases


@pytest.mark.parametrize(
    'tree, lines, expected',
    _load_test_cases(),
)
def test_styles(tree, lines, expected):
    checker = Linter(tree, lines)
    codes = set()
    for lineno, _, message, _ in checker.run():
        code, _ = message.split(' ', 1)
        codes.add((lineno, code))
    assert codes == expected
