Installation
============

This guideline introduce how to install ugoira.

Prerequisites
-------------

Ugoira is made with the following softwares:

Python_ 3.3 or higher
   ugoira is mostly written in Python language.  It's a high-level scripting
   language for general purpose. We recommend 3.5 or higher because
   we use 3.5.0 in develop.

Newest version of Imagemagick_
   ugoira's image generator use Imagemagick internally. It's a image
   manipulation toolkit.

Mac OS X
++++++++

If you're using Mac, you can find CPython installer in Python_ website's
download page and you can find Imagemagick_ installer in Homebrew_.

.. sourcecode:: console

   $ brew install imagemagick


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
   $ sudo apt-get install python3 libmagickwand-dev


.. _Imagemagick: http://www.imagemagick.org/script/index.php
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

