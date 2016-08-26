from distutils.core import setup
import py2exe, sys, os

sys.argv.append('py2exe')

setup(
    options = {'py2exe': {'optimize': 2}},
    windows = [{'script': "Annin Robot.py","icon_resources": [(1, "ARbot.ico")]}],
    zipfile = "shared.lib",
)