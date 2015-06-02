.. highlight:: rst
System Hotkeys
==============

'Multiplatform system wide hotkeys'

Atm support x11 and windows. Osx support is coming in a few years i would say!

Installation
^^^^^^^^^^^^

For windows you will need to install pywin32

For x11 you will should probably use the xcffib library, you will need the xcb bindings (bsd license) installed to use it (i think???)
Also supported is the python xlib bindings (gpl license)

then do the old pip3 install system_hotkeys

Usage:
^^^^^^
			from system_hotkey import SystemHotkeys

			hk = SystemHotkeys()
			hk.register(('control', 'shift', 'h'), callback=lambda:print("Easy hotkeys 123!!!"))
			hk.unregister(('control', 'shift', 'h'))

To not use the callback sytem you can do something like this

     def some_func(self, event, hotkey, args):	
	     self.do_something(hotkey)	
			
     hk = SystemHotkeys(consumer=some_func)
     
 .. highlight:: rst

============================
reStructuredText with Sphinx
============================

-----------------
Setting up Sphinx
-----------------

^^^^^^^^^^
Windows XP
^^^^^^^^^^

* Install `Python 2.7 <http://www.python.org/ftp/python/2.7/python-2.7.msi>`_
* Install `Python Setuptools <http://pypi.python.org/packages/2.7/s/setuptools/setuptools-0.6c11.win32-py2.7.exe#md5=57e1e64f6b7c7f1d2eddfc9746bbaf20>`_ (a package manager)
* Set PATH environment variable for Python scripts:

  - Right-click *My Computer*
  - Click *Properties*
  - Go to the *Advanced* tab
  - Click the *Environment Variables* button
  - From *System Variables*, select *Path*, and click *Edit*
  - Assuming you installed Python to ``C:\Python27`` (the default), add this to the end of *Variable value*::

       ;C:\Python27;C:\Python27\Scripts

* Launch the terminal: Click *Start*, then *Run*, write ``cmd``, press Enter.
* Install Sphinx by typing the following commands to the terminal::

     easy_install pip
     pip install sphinx

* Do not close the terminal, you are going to need it.

^^^^^^^^^
Windows 7
^^^^^^^^^

* Install `Python 2.7 <http://www.python.org/ftp/python/2.7/python-2.7.msi>`_
* Install `Python Setuptools <http://pypi.python.org/packages/2.7/s/setuptools/setuptools-0.6c11.win32-py2.7.exe#md5=57e1e64f6b7c7f1d2eddfc9746bbaf20>`_ (a package manager)
* Set PATH environment variable for Python scripts:

  - Right-click *Computer*
  - Click *Properties*
  - Go to the *Advanced system settings* tab
  - Click the *Environment Variables* button
  - From *System Variables*, select *Path*, and click *Edit*
  - Assuming you installed Python to ``C:\Python27`` (the default), add this to the end of *Variable value*::

       ;C:\Python27;C:\Python27\Scripts

* Launch the terminal: Click *Start*, find *Powershell*, click it.
* Install Sphinx by typing the following commands to the terminal. There might be some errors, those should not be a problem (probably)::

     easy_install pip
     pip install sphinx

* Do not close the terminal, you are going to need it.

^^^^^^^^^^^^^^^
Debianoid Linux
^^^^^^^^^^^^^^^

* Python is installed (Unless you're using a brutally lightweight distro. Probably not ideal for documentation production).
* Install Sphinx by typing the following commands to the terminal::
  
     sudo apt-get install python-pip
     sudo pip install sphinx
      

--------------------------
Creating the documentation
--------------------------

* Now, still in the terminal, create a directory for your documentation and move there.

  Windows XP::

     md mydoc
     cd mydoc

  Win7/Linux::

     mkdir mydoc
     cd mydoc

* And finally generate a basic documentation template::

     sphinx-quickstart

* Quickstart will ask you some questions.
  The only questions that should interest you for now are:

  - *Project name:*
  - *Author name:*  
  - *Project version*

  You can skip the others by pressing Enter.
  This will set up default settings.

  You can change any of these options later (you will be changing at least the version as your project develops).
  
* This created a documentation source directory. 
  Important files in this directory:

  ===============  =======================================================================
  Directory        Contents
  ===============  =======================================================================
  ``conf.py``      Documentation configuration file.
  ``index.rst``    Documentation master file.
  ``Makefile``     Make file to generate documentation on Linux/Unix.
  ``make.bat``     Batch file to generate documentation on Windows.
  ===============  =======================================================================

* The master document, ``index.rst``, serves as a table of contents and
  welcome page for the documentation. 

  It contains a heading, table of contents, and a section called
  *Indices and Tables* with references for module index, search and so on.

  You probably won't need the *Indices and Tables* section for now, so I
  recommend to remove it. (This section is added with Python documentation
  in mind - getting module index and search to work for non-Python documentation
  would need some googling.)


  reStructuredText depends on indentation. For example,
  below, each entry in the table of contents has the same indentation.
  This is always **3 spaces**, no tabs. Less or more might work, or it might not.

  By default, the table of contents should look like this::

     Contents:

     .. toctree::
       :maxdepth: 2

  You can add documents to the table of contents like this::
     
     Contents:

     .. toctree::
       :maxdepth: 2

       tutorial

  ``tutorial`` refers to a document called ``tutorial.rst`` in the documentation directory.

  Example table of contents from a real project::

     Tutorials:
     
     .. toctree::
        :maxdepth: 2
     
        tutorials/getting_started
        tutorials/custom_types 
        tutorials/yaml_syntax 
     
     Articles:
     
     .. toctree::
        :maxdepth: 2
     
        articles/spec_differences

  Here we see documents in subdirectories of the documentation directory.


* Now create some content.

  Create a new reStructuredText file, for example ``example.rst``, in the documentation directory.
  Add it to table of contents (add ``example`` to ``toctree`` in ``index.rst``.)

  Open the file in any text editor (MS Word is not a text editor).
  When saving the file, **make sure** to use the UTF-8 encoding. 

  Use `source code of this tutorial <https://raw.github.com/kiith-sa/reStructuredText-tutorial/master/README.rst>`_ 
  as a reference.

  Use ``Ctrl-C`` and ``Ctrl-V`` . Do random stuff to try what does what.


  For example you can do this:

  * Text::
    
       An extremely awesome sentence. Another mega-awesome sentence.
       Lines that are together form a paragraph.
    
       Lines that are apart form separate paragraphs.

  * *emphasized text* : ``*emphasized text*``
  * **strong text**   : ``**strong text**``
  * ``literal text``  :: 

     ``literal text``

  * `A link <http://www.google.com>`_ : :: 

     `A link <http://www.google.com>`_

  * A code block (note the empty line and **3 spaces** of indentation)::

       A code block::
         
          print "Hello World!"

  * Headings::

       Level 1
       =======
       
       ===================================================
       This is level 1 too, but looks better in plain text
       ===================================================
       
       Level 2
       -------
       
       Level 3
       ^^^^^^^
       
       Level 4
       """""""

  * An image: ``.. image:: image.png``

  * Bullet lists::

       * this is
       * a list
       
         * with a nested list
         * and some subitems
       
       * and here the parent list continues

  * Numbered lists::
       
       1. This is a numbered list.
       2. It has two items too.
     
  * Can be automatically numbered::

       #. This is a numbered list.
       #. It has two items too.

  * Tables::
     
       ====== ============ =======
       No.    Availability Name
       ====== ============ =======
       1      N/A          Biros
       2      42           piskoty
       3      N/A          beton
       ====== ============ =======

  * Comments::
     
       .. my awesome comment

  * Citations (the citation itself must be at the end of file)::

       Here is a citation reference: [CIT2002]_.

       .. [CIT2002] This is the citation.

  For more stuff, see the `reStructuredText Primer <http://sphinx.pocoo.org/rest.html>`_ .


* Now generate the documentation.

  WinXP/Win7::

     .\make html

  Linux::

     make html

  This will generate the documentation in HTML format. To find out what other formats 
  are available, use make with no arguments:
     
  WinXP/Win7::

     .\make

  Linux::

     make 

  Among others, there should be HTML, LaTeX, Windows HTML Help (chm), man, and so on.

  The generated documentation will be found in the ``_build`` directory, each format
  in its own subdirectory (e.g. ``_build/html`` for HTML).


-------------------------------------------------------------
Some extra features interesting for programming documentation
-------------------------------------------------------------

^^^^^^^^^^^^^^^^^^^^^^^^
Source code highlighting
^^^^^^^^^^^^^^^^^^^^^^^^

The ``code-block`` directive can be used to highlight source code.
Just about any language is supported. E.g. ``c`` for C, ``cpp`` for C++,
``java`` for Java, also ``python``, ``ruby``, ``yaml``, ``xml``, etc, etc...

Example highighing D source code where we also use ``:linenos:`` to
get line numbers and ``:emphasize-lines:`` to emphasize lines 1, 2 and 4::

   .. code-block:: d
      :linenos:
      :emphasize-lines: 1,2,4
   
      import std.stdio;
      import yaml;
   
      void main()
      {
          //Read the input.
          Node root = Loader("input.yaml").load();
   
          //Display the data read.
          foreach(string word; root["Hello World"])
          {
              writeln(word);
          }
          writeln("The answer is ", root["Answer"].as!int);
   
          //Dump the loaded document to output.yaml.
          Dumper("output.yaml").dump(root);
      }

^^^^^^^^^^^^^^^^
Cross-file links
^^^^^^^^^^^^^^^^

Sections can be labelled by labels in format ``.. _LABELNAME:``, 
where LABELNAME is the name of your label (duh).

They can be referenced like this: ``:ref:`LABELNAME``` . 

Example::

   .. _the-awesome-section:

   This Section is Awesome
   -----------------------
   
   This text is awesomely recursive: :ref:`the-awesome-section`


This works even across different files.

This is better than plain links because it works even if files get renamed.


---------------------
Example documentation
---------------------

* `Python documentation <http://docs.python.org/>`_
* `Zope documentation <http://docs.zope.org/zope2/index.html>`_
* `D:YAML documentation <http://dyaml.alwaysdata.net/static/html/doc_0.4/index.html>`_

-----
Links
-----

* `Sphinx <http://sphinx.pocoo.org>`_
* `Sphinx tutorial <http://sphinx.pocoo.org/tutorial.html>`_
* `reStructuredText Primer <http://sphinx.pocoo.org/rest.html#rst-primer>`_
* `Quick reStructuredText reference <http://docutils.sourceforge.net/docs/user/rst/quickref.html>`_ 
* `Sphinx documentation <http://sphinx.pocoo.org/contents.html>`_
* `rst2pdf (generates PDF from reStructuredText) <http://code.google.com/p/rst2pdf/>`_


