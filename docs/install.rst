Installation
============

This guideline introduce how to install ugoira.

Prerequisites
-------------

Ugoira is made with the following softwares:

Python_ 3.4 or higher
   ugoira is mostly written in Python language.  It's a high-level scripting
   language for general purpose. ugoira tested in Python 3.4, 3.5, 3.6 and 3.7.

`Imagemagick 6`_
   ugoira use Imagemagick 6 for generate gif image. It's a image
   manipulation toolkit.

Mac OS X
++++++++

If you're using Mac, you can find CPython installer in Python_ website's
download page and you can find `Imagemagick 6`_ installer in Homebrew_.

.. sourcecode:: console

   $ brew install imagemagick@6


Windows
+++++++

If you're using Windows you can find CPython installer in Python_ website's
download page. In installation process, You **must** check install with pip
and add Python_ into :const:`PATH`.


Debian/Ubuntu
+++++++++++++

If you’re using Linux distributions based on Debian like Ubuntu,
it can be easily installed using APT:

.. sourcecode:: console

   $ sudo apt-get update
   $ sudo apt-get install python3 libmagickwand6-dev


.. _`Imagemagick 6`: http://www.imagemagick.org/script/index.php
.. _Homebrew: http://brew.sh/
.. _Python: https://www.python.org/


Install with pip
----------------

Now we can install ugoira by command line. If you use Windows, open
the ``cmd``. If you use Mac OS X or Linux, open the terminal, And type this

.. sourcecode:: console

   $ pip3 install ugoira

Install is completed. You can test it by this command.

.. sourcecode:: console

   $ ugoira --help

