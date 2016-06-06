from setuptools import setup, find_packages
from codecs import open 					
import os
here = os.path.abspath(os.path.dirname(__file__))

def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths), 'r') as f:
        return f.read()

#if os.name == 'nt':
#	REQUIRED = ['pywin32']
#else:
REQUIRED = []

setup(
	name = 'system_hotkey',

	version='1.0.1',
	
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
		'Development Status :: 3 - Alpha',
		'Intended Audience :: Developers',
		'Operating System :: OS Independent',
		'License :: OSI Approved :: BSD License',
		# Specify the Python versions you support here. In particular, ensure
		# that you indicate whether you support Python 2, Python 3 or both.
		#~ 'Programming Language :: Python :: 2',
		#~ 'Programming Language :: Python :: 2.6',
		#~ 'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.2',
		'Programming Language :: Python :: 3.3',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
	],

	# What does your project relate to?
	keywords = 'hotkeys python3 shortcutkeys shortuct x11 windows',

	# You can just specify the packages manually here if your project is
	# simple. Or you can use find_packages().
	packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
	
	# List run-time dependencies here. These will be installed by pip when your
	# project is installed. For an analysis of "install_requires" vs pip's
	# requirements files see:
	# https://packaging.python.org/en/latest/requirements.html
	install_requires = REQUIRED,
	
	# List additional groups of dependencies here (e.g. development dependencies).
	# You can install these using the following syntax, for example:
	# $ pip install -e .[dev,test]
	#~ extras_require = {
	#~ 'dev': ['check-manifest'],
	#~ 'test': ['coverage'],
	#~ },
	
	# If there are data files included in your packages that need to be
	# installed, specify them here. If using Python 2.6 or less, then these
	# have to be included in MANIFEST.in as well.
	#~ package_data={
	#~ 'sample': ['package_data.dat'],
	#~ },
	
	# Although 'package_data' is the preferred approach, in some case you may
	# need to place data files outside of your packages.
	# see http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files
	# In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
	#~ data_files=[('my_data', ['data/data_file'])],
	
	# To provide executable scripts, use entry points in preference to the
	# "scripts" keyword. Entry points provide cross-platform support and allow
	# pip to create the appropriate form of executable for the target platform.
	#~ entry_points = {
			#~ 'console_scripts': [
				#~ 'sample=sample:main',],},
)
