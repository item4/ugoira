Usage
=====

Understanding about ``image-id``
--------------------------------

ugoira needs ``image-id`` for download target.

First, Open pixiv page what you want to download. Then you can see the url at
url bar of browser like this.

``http://www.pixiv.net/member_illust.php?mode=medium&illust_id=44522595``

Look at the number after ``illust_id=``, ``44525295`` is ``image-id``!

``image-id`` must be integer, must not include other character such as ``&``,
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


Image animation Speed-Up
++++++++++++++++++++++++

You can change animation speed with ``--div-by`` option.

For example, if you want to increase speed by 10x, type it.

.. sourcecode:: console

   $ ugoira --div-by 10 44525295 toramaru.gif


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
