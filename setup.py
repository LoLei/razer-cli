"""razer-cli - setup.py"""
from setuptools import setup, find_packages

LONG_DESC = open('README.md').read()

setup(
    name="razer-cli",
    version="2.0.0",
    author="Lorenz Leitner",
    author_email="lrnz.ltnr@gmail.com",
    description="Control Razer devices from the command line",
    long_description_content_type="text/markdown",
    long_description=LONG_DESC,
    url="https://github.com/lolei/razer-cli",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(),
    entry_points={"console_scripts": ["razer-cli=razer_cli.razer_cli.razer_cli:main"]},
    python_requires=">=3.7",
    package_data={'': ['razer_cli/razer_cli/man_pages']},
    include_package_data=True,
    )
