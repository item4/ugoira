""":mod:`ugoira.cli` --- Ugoira Download Command Line
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This provide ugoira download command line executable :program:`ugoira`:

.. sourcecode:: console

   $ ugoira
   Usage: ugoira [OPTIONS] ILLUST_ID DEST

.. describe:: ILLUST_ID

   ``illust-id`` of your wants to download.
   It can get from Pixiv image url. see ``illust-id`` parameter in url.

.. describe:: DEST

   The saving path of generated file by work.
   If DEST's suffix is ``.zip``, ugoira generate ZIP file.
   If DEST's suffix is ``.gif`` or not match any cases, ugoira generate
   GIF image.

There are options as well:

.. option:: --acceleration <speed>

   You can accelerate GIF speed using this option.
   For example, if you given it 10, GIF fasten 10x.
   Default is :const:`1.0`.

"""

from .lib import PixivError, download_zip, is_ugoira, make_gif, save_zip

from click import Path, argument, command, echo, option


__all__ = 'ugoira',


@command()
@option('--acceleration', type=float, default=1.0,
        help='You can accelerate interval between images by using this option.'
             ' Default value is 1.0 (default speed)')
@argument('illust-id', type=int)
@argument('dest', type=Path())
def ugoira(acceleration: float,
           illust_id: int,
           dest: str):
    """ugoira command for download Pixiv Ugokuillust."""

    if is_ugoira(illust_id):
        blob, frames = download_zip(illust_id)
        if dest.endswith('.zip'):
            save_zip(dest, blob)
            echo('download completed at {} as zip'.format(dest))
        else:
            if not dest.endswith('.gif'):
                dest += '.gif'

            make_gif(dest, blob, frames, acceleration)
            echo('download completed at {} as gif'.format(dest))
    else:
        echo('Given illust-id is not ugoira.', err=True)
        raise SystemExit(1)
