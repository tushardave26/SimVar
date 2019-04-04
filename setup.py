from setuptools import setup

setup(
    name='SimVar',
    version='0.0.1',
    author='Tushar Dave',
    author_email='tushardave26@gmail.com',
    py_modules=['simvar.py'],
    install_requires=[
        "click==7.0",
        "pybedtools==0.8.0",
    ],
    entry_points='''
        [console_scripts]
        simvar=simvar.py:cli
    ''',
)