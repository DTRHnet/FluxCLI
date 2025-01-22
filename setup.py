from setuptools import setup, find_packages

setup(
    name="fluxcli",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "PyYAML",
        # any other dependencies, e.g. "requests", etc.
    ],
    entry_points={
        "console_scripts": [
            "fluxcli = fluxcli.main:main"
        ]
    }
)
