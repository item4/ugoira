Installation
============

This guide introduces how to install ugoira.

Prerequisites
-------------

Ugoira is made with the following softwares:

Python_ 3.8 or higher
   ugoira is mostly written in Python language, a high-level general-purpose scripting
   language. ugoira was tested in Python 3.8 and 3.9.

`Imagemagick 7`_
   ugoira uses Imagemagick 7 to generate gif images. It's an image
   manipulation toolkit.

Mac OS X
++++++++

If you're using Mac, you can find CPython installer in Python_ website's
download page and you can find `Imagemagick 7`_ installer in Homebrew_.

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


.. _`Imagemagick`: http://www.imagemagick.org/script/index.php
.. _Homebrew: http://brew.sh/
.. _Python: https://www.python.org/


Install with pip
----------------

Now we can install ugoira by command line. If you use Windows, open
the ``cmd``. If you use Mac OS X or Linux, open the terminal, And type this

.. sourcecode:: console

   $ pip3 install ugoira

If you want to handle apng format, Type this

.. sourcecode:: console

   $ pip3 install ugoira[apng]

Install is completed. You can test it by issuing this command.

.. sourcecode:: console

   $ ugoira --help

