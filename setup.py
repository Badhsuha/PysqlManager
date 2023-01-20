from setuptools import setup, find_packages

setup(
    name='pysql_manager',
    version='0.1.1',
    description='A python package for managing Mysql',
    url='https://github.com/Badhsuha/PysqlManager',
    author='Badhusha K Muhammed',
    author_email='badhushamuhammed09@gmail.com',
    license='BSD 2-clause',
    install_requires=['mysql-connector-python',
                      'pandas',
                      'numpy'
                      ],
    packages=find_packages(),

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
)