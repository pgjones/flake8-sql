import os

from setuptools import setup, find_packages

PROJECT_ROOT = os.path.dirname(__file__)

with open(os.path.join(PROJECT_ROOT, 'flake8_sql', 'linter.py')) as file_:
    version_line = [line for line in file_ if line.startswith('__version__')][0]

__version__ = version_line.split('=')[1].strip().strip("'").strip('"')

with open(os.path.join(PROJECT_ROOT, 'README.rst')) as file_:
    long_description = file_.read()

setup(
    name='flake8-SQL',
    version=__version__,
    description='Flake8 plugin that checks SQL code against opinionated style rules',
    long_description=long_description,
    url='https://github.com/pgjones/flake8-sql',
    author='P G Jones',
    author_email='philip.graham.jones@googlemail.com',
    keywords=[
        'flake8',
        'plugin',
        'sql',
    ],
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Framework :: Flake8',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Quality Assurance',
    ],
    packages=find_packages(exclude=["tests", "tests.*"]),
    py_modules=['flake8_sql'],
    install_requires=[
        'flake8',
        'setuptools',
        'sqlparse',
    ],
    entry_points={
        'flake8.extension': [
            'Q4 = flake8_sql:Linter',
        ],
    },
    zip_safe=False,
)
