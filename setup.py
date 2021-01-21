"""razer-cli - setup.py"""
import setuptools

LONG_DESC = open('README.md').read()

setuptools.setup(
    name="razer-cli",
    version="1.5.0",
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
    packages=["razer_cli"],
    entry_points={"console_scripts": ["razer-cli=razer_cli.razer_cli:main"]},
    python_requires=">=3"
    )
