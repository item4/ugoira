""":mod:`ugoira.cli` --- Ugoira Download Command Line
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This provides a command-line executable :program:`ugoira`:

.. sourcecode:: console

   $ ugoira
   Usage: ugoira [OPTIONS] ILLUST_IDS

.. describe:: ILLUST_ID

   ``illust-id`` of the image you want to download.
   It can be retrieved from Pixiv image URLs.
   See ``illust-id`` parameter in URL.

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
    default='{}.{}',
    help='A format string specifying the path of downloaded files.'
         ' The illust ID and your chosen format will replace'
         ' {}s in it, if any.'
         ' Default is \'./{}.{}\'.'
)
@argument('illust-ids', type=int, nargs=-1)
def ugoira(
    speed: float,
    format: str,
    dest: Optional[str],
    illust_ids: tuple,
):
    """ugoira command to download Pixiv Ugokuillusts."""
    for i, illust_id in enumerate(illust_ids):
        echo("Downloading {} ({}/{})".format(illust_id, i, len(illust_ids)))
        if is_ugoira(illust_id):
            try:
                blob, frames = download_ugoira_zip(illust_id)
            except PixivError as e:
                echo('Error: {}'.format(e), err=True)
                continue

            filename = dest.format(illust_id, format)

            save(format, filename, blob, frames, speed)
            echo(
                'Download was completed successfully.'
                ' format is {} and output path is {}'.format(
                    format,
                    filename,
                )
            )
        else:
            echo('Illust ID {} is not ugoira.'.format(illust_id), err=True)
