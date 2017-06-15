from setuptools import setup

setup(
    name='blockfolio',
    version='1.0.0',
    description='Blockfolio CLI',
    url='https://github.com/banteg/blockfolio',
    py_modules=['blockfolio'],
    install_requires=[
        'click',
        'requests',
        'tabulate',
    ],
    entry_points={
        'console_scripts': [
            'blockfolio = blockfolio:main',
        ],
    }
)
