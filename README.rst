Ugoira
======

.. image:: https://readthedocs.org/projects/ugoira/badge/?version=latest
   :target: http://ugoira.readthedocs.org/

.. image:: https://travis-ci.org/item4/ugoira.svg?branch=master
   :target: https://travis-ci.org/item4/ugoira

.. image:: https://img.shields.io/coveralls/item4/ugoira.svg?
   :target: https://coveralls.io/r/item4/ugoira

Ugoira is download tool for Pixiv Ugoira.
Pixiv Ugoira is **Ugoku** (Animated) Illustration.

If you need more detail information, `See the docs for details`__.

__ http://ugoira.readthedocs.org/en/latest/


Simple Installation
-------------------

1. Install Imagemagick

   I use Wand. It need Imagemagick. Please see `Wand install guide`__

   __ http://docs.wand-py.org/en/0.4.1/guide/install.html

2. Install

   .. code-block:: console

      $ pip install ugoira


Usage
-----

.. code-block:: console

   $ ugoira illust-id filename.gif


For Developer
-------------

You must install Tests Requirements.

.. code-block:: console

   $ pip install -e .[tests]


License
-------

MIT
