import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

url = 'https://github.com/QueraTeam/sql-judge-utils'

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='sql-judge-utils',
    version='0.1.5',
    packages=find_packages(
        exclude=(
            'tests'
        )
    ),
    include_package_data=True,
    description='A reusable python package for problem design and judge of quera sql problems',
    long_description_content_type='text/markdown',
    long_description=README,
    url=url,
    author='Quera',
    author_email='info@quera.ir',
    install_requires=[
        'psycopg2>=2.9.1',
        'mysql-connector-python>=8.0.25'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.9',
    ],
)

