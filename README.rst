Flake8-SQL
==========

|Build Status|

Flake8-SQL is a `flake8 <http://flake8.readthedocs.org/en/latest/>`__
plugin that looks for SQL queries and checks then against some
opinionated styles. These styles mostly follow `SQL Style
Guide <http://www.sqlstyle.guide/>`__, but differ as detailed below.

Warnings
--------

Q440 Keyword is not uppercase
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

All the SQL reserved
`keywords <https://github.com/pgjones/flake8-sql/blob/master/flake8_sql/keywords.py>`__
should be uppercase.

Q441 Name is not valid
~~~~~~~~~~~~~~~~~~~~~~

All the non SQL keywords should be snake\_case, start with a letter
and not end with an `\_`. Due to a limitation snake\_case is checks
ensure that the word is lowercase.

Q442 Avoid abbreviated keywords
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Avoid using `abbreviated
keywords <https://github.com/pgjones/flake8-sql/blob/master/flake8_sql/keywords.py>`__
instead use the full length version.

Q443 Incorrect whitespace around comma
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Commas should be followed by whitespace, but not preceded.

Q444 Incorrect whitespace around equals
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Equals should be surrounded with whitespace.

Q445 Missing linespace between root keywords
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The root keywords ``SELECT``, ``FROM``, ``INSERT``, ``VALUES``, ``DELETE
FROM``, ``WHERE``, ``UPDATE``, ``AND``, ``OR`` and ``SET`` should be
on separate lines (unless the entire query is on one line).

Q446 Missing newline after semicolon
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Semicolons must be at the end of the line.

Q447 Root keywords should be right aligned
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The root keywords ``SELECT``, ``FROM``, ``INSERT``, ``VALUES``,
``WHERE``, ``UPDATE``, ``AND``, ``OR``, ``JOIN`` and ``SET`` should be
right aligned i.e.

    SELECT *
      FROM table

Q448 subquery should be aligned to the right of the river
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Any subquery should be aligned to the right of the river i.e.

    SELECT *
      FROM table
     WHERE column IN
           (SELECT column
              FROM table)

Q449 tokens should be aligned to the right of the river
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Any tokens should be aligned to the right of the river i.e

    SELECT column1,
           column2
      FROM table

Configuration
-------------

At times it is simpler to use a reserved keyword as an identifier than
go to the effort to avoid it. To allow for this set the
``sql-excepted-names`` option to a comma separated list of these
names.


Limitations
-----------

String constants are sought out in the code and considered SQL if they
contain select from, insert into values, update set or delete from in
order. This may and is likely to lead to false positives, in which case
simply add ``# noqa`` to have this plugin ignore the string.

.. |Build Status| image:: https://travis-ci.org/pgjones/flake8-sql.svg?branch=master
   :target: https://travis-ci.org/pgjones/flake8-sql
