Usage
=====

Understanding ``illust-id``
---------------------------

:program:`ugoira` needs ``illust-id`` for download target.

First, Open pixiv page of the ugoira you want to download. Then you can see the url at
url bar of browser like this.

``https://www.pixiv.net/artworks/44522595``

Look at the number after ``/artworks/``, ``44525295`` is ``illust-id``!

``illust-id`` must be integer and must not include other characters such as ``&`` or
english alphabets.


Basic Download
--------------

You can download ugoira as GIF as default settings.
If you want to download the ``44525295`` as GIF, type it on
``cmd`` or terminal.

.. sourcecode:: console

   $ ugoira 44525295

If you can't find the file, type this.

.. sourcecode:: console

   $ pwd

Limitation of GIF
+++++++++++++++++

GIF only supports 256 colors in an image.
If you download a colorful ugoira as GIF, the downloaded image will be discolored
and lose some of its colors.


Download as other file formats
------------------------------

You can can also download ugoira as other formats, and you can use these formats:

* ``gif``: GIF (default)
* ``webp``: WEBP (lossless)
* ``apng``: APNG (lossless)
* ``pdf``: PDF (collection of each frames per page)
* ``zip``: ZIP (collection of each frames)

.. sourcecode:: console

   $ ugoira --format=webp 44525295
   $ ugoira --format=apng 44525295
   $ ugoira --format=pdf 44525295
   $ ugoira --format=zip 44525295

.. _webp library: https://developers.google.com/speed/webp/


Known issues
++++++++++++

1. Generating lossless format is slower than GIF because lossless format will generate best quality output.


Change Frame Interval
+++++++++++++++++++++

Sometimes, you might feel that the animation is too fast or too slow.
You can change interval of each frames to change animation speed with ``--speed`` option.

For example, if you want to accelerate the speed by 10x, give 10:

.. sourcecode:: console

   $ ugoira --speed 10 44525295


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


Download multiple ugoira at once
--------------------------------

If you want to download multiple ugoira by one command, you just pass multiple illust-ids to the command separated by spaces:

.. sourcecode:: console

   $ ugoira 44525295 44525296
