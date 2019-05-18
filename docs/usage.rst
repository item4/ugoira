Usage
=====

Understanding ``illust-id``
---------------------------------

:program:`ugoira` needs ``illust-id`` for download target.

First, Open pixiv page of the ugoira you want to download. Then you can see the url at
url bar of browser like this.

``http://www.pixiv.net/member_illust.php?mode=medium&illust_id=44522595``

Look at the number after ``illust_id=``, ``44525295`` is ``illust-id``!

``illust-id`` must be integer and must not include other characters such as ``&`` or
english alphabets.


Download as GIF
---------------

You can download ugoira as GIF.
If you want to download the ``44525295`` as GIF, type it on
``cmd`` or terminal.

.. sourcecode:: console

   $ ugoira 44525295

If you can't find the file, type this.

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

If you can't find the file, type this.

.. sourcecode:: console

   $ pwd


Change Frame Interval
+++++++++++++++++++++

You can change interval of each frames to change animation speed with ``--speed`` option.

For example, if you want to accelerate the speed by 10x, give 10:

.. sourcecode:: console

   $ ugoira --speed 10 44525295


Limitation of GIF
+++++++++++++++++

GIF only supports 256 colors in an image.
If you download a colorful ugoira as GIF, the downloaded image will be discolored
and lose some of its colors.


Download as ZIP
---------------

You can download ugoira as ZIP.
If you want to download the ``44525295`` as ZIP, type it on
``cmd`` or terminal.

.. sourcecode:: console

   $ ugoira --format=zip 44525295

If you can't find the file, type this.

.. sourcecode:: console

   $ pwd


Change result filename and path
-------------------------------

You can change filename and path with ``--dest`` option.

.. sourcecode:: console

   $ ugoira --dest=toramaru.gif 44525295

{}s in the option are replaced with the illust-id and format.
You may find this useful when downloading multiple files at once.

.. sourcecode:: console

   $ ugoira --dest=number_{}_ugoira.{} 44525295

In the example above, the output filename would be 'number_44525295_ugoira.gif'.


Download multiple files
-----------------------

Simply pass multiple illust-ids:

.. sourcecode:: console

   $ ugoira 44525295 44525296
