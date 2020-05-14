from os import path
from setuptools import setup
from binaryclock import clock


here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


setup(
    name="binaryclock",
    version=clock.__version__,
    packages=["binaryclock"],
    description="Binary Clock with Tkinter",
    long_description=long_description,
    url=clock.__source__,
    author=clock.__author__,
    author_email=clock.__contact__,
    platforms=["Linux"],
    keywords="tkinter binary clock",
    package_data={"binaryclock": ["data/*.*"]},
    data_files=[
        ("share/icons", ["binaryclock/data/binaryclock.png"]),
        ("share/applications", ["binaryclock.desktop"]),
    ],
    entry_points={"gui_scripts": ["binaryclock = binaryclock:launch"]},
)
