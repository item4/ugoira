from setuptools import find_packages, setup

install_requires = {
    'click >= 5.1',
    'requests >= 2.8.1',
    'Wand >= 0.4.1',
}

tests_require = {
    'pytest >= 2.8.2',
    'httpretty >= 0.8.10',
}

extras_require = {
    'tests': tests_require,
}

setup(
    name='ugoira',
    version='0.0.0',
    description='ugoira for download pixiv ugoira images',
    url='https://github.com/item4/ugoira',
    packages=find_packages(),
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require=extras_require,
    entry_points={
        'console_scripts': [
            'ugoira=ugoira.cli:ugoira',
        ],
    },
)
