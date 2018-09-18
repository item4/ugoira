from setuptools import find_packages, setup

install_requires = [
    'click ~= 6.7',
    'requests ~= 2.19.1',
    'Wand ~= 0.4.4',
]

tests_require = [
    'pytest ~= 3.8.0',
    'responses ~= 0.9.0',
    'flake8 ~= 3.5.0',
]

docs_requires = [
    'Sphinx ~= 1.8.0',
]

extras_require = {
    'tests': tests_require,
    'docs': docs_requires,
}

setup(
    name='ugoira',
    author='item4',
    author_email='item4_hun' '@' 'hotmail.com',
    version='0.2.0',
    description='ugoira for download pixiv ugoira images',
    long_description=open('README.rst').read(),
    url='https://github.com/item4/ugoira',
    download_url='https://github.com/item4/ugoira/tarball/0.2.0',
    license='MIT',
    packages=find_packages(),
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require=extras_require,
    entry_points={
        'console_scripts': [
            'ugoira=ugoira.cli:ugoira',
        ],
    },
    keywords=[
        'pixiv',
        'ugoira'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Multimedia :: Graphics',
    ],
)
