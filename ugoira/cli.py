""":mod:`ugoira.cli` --- Ugoira Download Command Line
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This provide ugoira download command line executable :program:`ugoira`:

.. sourcecode:: console

   $ ugoira
   Usage: ugoira [OPTIONS] ILLUST_ID

.. describe:: ILLUST_ID

   ``illust-id`` of your wants to download.
   It can get from Pixiv image url. see ``illust-id`` parameter in url.

There are options as well:

.. option:: --speed <amount>

   If you want to make animated image file, you can
   divide seconds of each frames's interval.
   Default value is 1.0 (no change)

.. option:: --format <file_format>
.. option:: -f <file_format>

   Format of result file.
   You can select apng, gif, and zip format.
   Default value is gif.

.. option:: --dest <path>
.. option:: -d <path>

   Path of output file.
   Default is ``./<illust-id>.<format>``\.

"""
from typing import Optional

from click import Path, argument, command, echo, option

from .lib import PixivError, download_ugoira_zip, is_ugoira, save

__all__ = 'ugoira',


@command()
@option(
    '--speed',
    type=float,
    default=1.0,
    help="If you want to make animated image file, "
         "you can divide seconds of each frames's interval."
         " Default value is 1.0 (no change)",
)
@option(
    '--format',
    '-f',
    type=str,
    default='gif',
    help='Format of result file.'
         ' You can select apng, gif, and zip format.'
         ' Default value is gif.'
)
@option(
    '--dest',
    '-d',
    type=Path(),
    help='Path of output file. Default is `./<illust-id>.<format>`.',
)
@argument('illust-id', type=int)
def ugoira(
    speed: float,
    format: str,
    dest: Optional[str],
    illust_id: int,
):
    """ugoira command for download Pixiv Ugokuillust."""

    if is_ugoira(illust_id):
        try:
            blob, frames = download_ugoira_zip(illust_id)
        except PixivError as e:
            echo('Error: {}'.format(e), err=True)
            raise SystemExit(1)

        if dest is None:
            dest = '{}.{}'.format(illust_id, format)

        save(format, dest, blob, frames, speed)
        echo(
            'Download was completed successfully.'
            ' format is {} and output path is {}'.format(
                format,
                dest,
            )
        )
    else:
        echo('Given illust-id is not ugoira.', err=True)
        raise SystemExit(1)
