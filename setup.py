from setuptools import setup, find_packages
from codecs import open
import os
here = os.path.abspath(os.path.dirname(__file__))

def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths), 'r') as f:
        return f.read()

setup(
	name = 'system_hotkey',
	version='1.0.3',
	description = 'System wide hotkeys',
	long_description = (read('README.rst') + '\n\n' +
                      read('HISTORY.rst') + '\n\n' +
                      read('AUTHORS.rst')),
	url = 'https://github.com/timeyyy/system_hotkey',
	author='timothy eichler',
	author_email='tim_eichler@hotmail.com',
	license='BSD3',
	# See https://pypi.python.org/pypi?%3Aaction=list_classifiers
	classifiers=[
		# How mature is this project? Common values are
		#~ 3 - Alpha
		# 4 - Beta
		# 5 - Production/Stable
		'Development Status :: 4 - Beta',
		'Intended Audience :: Developers',
		'Operating System :: OS Independent',
		'License :: OSI Approved :: BSD License',
		#~ 'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 3',
	],

	# What does your project relate to?
	keywords = 'hotkeys python3 shortcutkeys shortuct x11 windows',
	packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
)
