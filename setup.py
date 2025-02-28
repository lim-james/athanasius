# setup.py
from setuptools import setup, find_packages

setup(
    name="athanasius",
    version="0.1.0",
    description="python CLI to archiving files",
    author="James",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[],
    entry_points={
        "console_scripts": [
            "ath=athanasius.cli:main",
        ],
    },
)
