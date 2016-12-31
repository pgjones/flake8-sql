# Flake8-SQL

[![Build Status](https://travis-ci.org/pgjones/flake8-sql.svg?branch=master)](https://travis-ci.org/pgjones/flake8-sql)

Flake8-SQL is a [flake8](http://flake8.readthedocs.org/en/latest/)
plugin that looks for SQL queries and checks then against some
opinionated styles. These styles mostly follow [SQL Style
Guide](http://www.sqlstyle.guide/), but differ as detailed below.

## Warnings

### Q440 Keyword is not uppercase

All the SQL reserved
[keywords](https://github.com/PyCQA/flake8-import-order/blob/master/flake8_sql/keywords.py)
should be uppercase.

### Q441 Name is not snake_case

All the non SQL keywords should be snake_case, which due to a
limitation means simply that the word is lowercase.

### Q442 Avoid abbreviated keywords

Avoid using [abbreviated
keywords](https://github.com/PyCQA/flake8-import-order/blob/master/flake8_sql/keywords.py)
instead use the full length version.

## Limitations

String constants are sought out in the code and considered SQL if they
contain select from, insert into values, update set or delete from in
order. This may and is likely to lead to false positives, in which
case simply add `# noqa` to have this plugin ignore the string.
