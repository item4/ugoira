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

.. option:: --id <id>

   Your Pixiv Account ID. It needs by Pixiv access.

   You can omit this option by export environment variable.

   In Linux/Mac

   .. sourcecode:: console

      $ export PIXIV_ID='item4'

   In Windows

   .. sourcecode:: console

      $ set PIXIV_ID='item4'

   If you omit this option without environment variable, ugoira show prompt to
   input ID.

.. option:: --password <password>

   Your Pixiv Account Password. It needs by Pixiv access.

   You can omit this option by export environment variable.

   In Linux/Mac

   .. sourcecode:: console

      $ export PIXIV_PASSWORD='supersecret'

   In Windows

   .. sourcecode:: console

      $ set PIXIV_PASSWORD='supersecret'

   If you omit this option without environment variable, ugoira show prompt to
   input Password.

.. option:: --acceleration <speed>

   You can accelerate GIF speed using this option.
   For example, if you given it 10, GIF fasten 10x.
   Default is :const:`1.0`.

"""

from .lib import PixivError, download_zip, is_ugoira, login, make_gif, save_zip

from click import Path, argument, command, echo, option


__all__ = 'ugoira',


@command()
@option('--id', prompt='Your Pixiv ID', help='Pixiv ID', envvar='PIXIV_ID')
@option('--password', prompt=True, hide_input=True, help='Pixiv Password',
        envvar='PIXIV_PASSWORD')
@option('--acceleration', type=float, default=1.0,
        help='You can accelerate interval between images by using this option.'
             ' Default value is 1.0 (default speed)')
@argument('illust-id', type=int)
@argument('dest', type=Path())
def ugoira(id: str,
           password: str,
           acceleration: float,
           illust_id: int,
           dest: str):
    """ugoira command for download Pixiv Ugokuillust."""

    try:
        login(id, password)
    except PixivError as e:
        echo(e, err=True)
        raise SystemExit(1)
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
