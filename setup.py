from setuptools import setup, find_packages
from pathlib import Path

this_dir = Path(__file__).parent
long_description = (this_dir / "README.md").read_text()

setup(
    name='pysql_manager',
    version='0.0.3',
    description='A python package for managing Mysql',
    url='https://github.com/Badhsuha/PysqlManager',
    author='Badhusha K Muhammed',
    author_email='badhushamuhammed09@gmail.com',
    install_requires=['mysql-connector-python',
                      'pandas',
                      'numpy'
                      ],
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
    license='BSD 3-Clause License',
    python_reuires=">= 3.6"
)