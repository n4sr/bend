from setuptools import setup, find_packages

from bend.version import VERSION


setup(
    name='bend',
    author='n4sr',
    version=VERSION,
    url='https://github.com/n4sr/bend',
    license='GPL-3.0-or-later',
    packages=find_packages(),
    python_requires='>=3.6',
    entry_points={'console_scripts': ['bend=bend.__main__:main']}
)
