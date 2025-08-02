#!/usr/bin/env python3

from setuptools import setup, find_packages
import os

# Read the contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="nitro-toolkit",
    version="2.0.3",
    author="HenryLok0",
    author_email="mail@henrylok.me",  # Replace with your email
    description="Discord Nitro gift code generator and checker toolkit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HenryLok0/nitro-toolkit",
    packages=find_packages() + [''],
    py_modules=['integrated_tool', 'discord_gift_checker'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.25.0",
        "colorama>=0.4.0",
    ],
    entry_points={
        "console_scripts": [
            "nitro-toolkit=integrated_tool:main",
            "nitro-checker=discord_gift_checker:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["data/*.txt", "*.md"],
    },
    keywords="discord nitro generator checker gift codes api",
    project_urls={
        "Bug Reports": "https://github.com/HenryLok0/nitro-toolkit/issues",
        "Source": "https://github.com/HenryLok0/nitro-toolkit",
        "Documentation": "https://github.com/HenryLok0/nitro-toolkit/blob/main/README.md",
    },
)
