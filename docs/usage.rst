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


Download as GIF
---------------

You can download ugoira as GIF.
If you want to download the ``44525295`` as GIF, type it on
``cmd`` or terminal.

.. sourcecode:: console

   $ ugoira 44525295

If you can not find where is the file exists, type this.

.. sourcecode:: console

   $ pwd


Download as APNG
----------------

You can download ugoira as APNG with extra dependency.
If you want to download the ``44525295`` as APNG, type it on
``cmd`` or terminal.

.. sourcecode:: console
   
   $ pip install ugoira[apng]
   $ ugoira --format=apng 44525295

If you can not find where is the file exists, type this.

.. sourcecode:: console

   $ pwd


Change Frame Interval
+++++++++++++++++++++

You can change interval of each frames for change animation speed with ``--speed`` option.

For example, if you want to acceleration speed by 10x, give 10 like it.

.. sourcecode:: console

   $ ugoira --speed 10 44525295


Limitation of GIF
+++++++++++++++++

GIF only support 256 color.
If you tried download colorful ugoira, downloaded image lost some color and
it must be discolored.


Download as ZIP
---------------

You can download ugoira as ZIP.
If you want to download the ``44525295`` as ZIP, type it on
``cmd`` or terminal.

.. sourcecode:: console

   $ ugoira --format=zip 44525295

If you can not find where is the file exists, type this.

.. sourcecode:: console

   $ pwd


Change result filename and path
-------------------------------

You can change filename and path by ``--dest`` option.

.. sourcecode:: console

   $ ugoira --dest=toramaru.gif 44525295
