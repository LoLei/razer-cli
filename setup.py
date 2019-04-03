"""razercli - setup.py"""
import setuptools

LONG_DESC = open('README.md').read()

setuptools.setup(
    name="razercli",
    version="0.0.8",
    author="Lorenz Leitner",
    author_email="test@gmail.com",
    description="Control Razer devices from the command line",
    long_description_content_type="text/markdown",
    long_description=LONG_DESC,
    url="https://github.com/lolei/razer-cli",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["razercli"],
    entry_points={"console_scripts": ["razercli=razercli.razercli:main"]},
    python_requires=">=3"
    )
