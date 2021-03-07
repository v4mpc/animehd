from setuptools import setup

setup(
    name='animehd',
    version='0.1',
    py_modules=['animehd'],
    install_requires=[
        'Click',
        'requests',
    ],
    entry_points='''
        [console_scripts]
        animehd=animehd:main
    ''',
)
