Usage
=====

Understanding about ``illust-id``
---------------------------------

:program:`ugoira` needs ``illust-id`` for download target.

First, Open pixiv page what you want to download. Then you can see the url at
url bar of browser like this.

``http://www.pixiv.net/member_illust.php?mode=medium&illust_id=44522595``

Look at the number after ``illust_id=``, ``44525295`` is ``illust-id``!

``illust-id`` must be integer, must not include other character such as ``&``,
english alphabets.


Download as GIF (Animated Image File)
-------------------------------------

You can download ugoira as GIF.
If you want to download the ``44525295`` to ``toramaru.gif``, type it on
``cmd`` or terminal.

.. sourcecode:: console

   $ ugoira 44525295 toramaru.gif

If you can not find where is the file exists, type this.

.. sourcecode:: console

   $ pwd


Image animation accelerate
++++++++++++++++++++++++++

You can accelerate animation speed with ``--acceleration`` option.

For example, if you want to acceleration speed by 10x, type it.

.. sourcecode:: console

   $ ugoira --acceleration 10 44525295 toramaru.gif


Limitation of GIF
+++++++++++++++++

GIF only support 256 color.
If you tried download colorful ugoira, downloaded image lost some color and
it must be discolored.


Download as ZIP
---------------

You can download ugoira as ZIP.
If you want to download the ``44525295`` to ``toramaru.zip``, type it on
``cmd`` or terminal.

.. sourcecode:: console

   $ ugoira 44525295 toramaru.zip

If you can not find where is the file exists, type this.

.. sourcecode:: console

   $ pwd

Skip typing ``ID`` and ``Password``
-----------------------------------

Do you want to do not repeat constantly typing ID and Password repeatly?

You can use environment variable.

In Linux/Mac

.. sourcecode:: console

   $ export PIXIV_ID='item4'
   $ export PIXIV_PASSWORD='supersecret'

In Windows

.. sourcecode:: console

   $ set PIXIV_ID='item4'
   $ set PIXIV_PASSWORD='supersecret'

Now you can use :program:`ugoira` without typing ID and Password.
