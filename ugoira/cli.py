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
   You can select ``apng``, ``gif``, ``pdf``, ``webp``, and ``zip`` format.
   Default value is ``gif``.

.. option:: --dest <path>
.. option:: -d <path>

   Path of output file.
   Default is ``./<illust-id>.<format>``.

"""

from pathlib import Path

from click import Path as ClickPath
from click import argument
from click import command
from click import echo
from click import option

from .lib import PixivError
from .lib import download_ugoira_zip
from .lib import save

__all__ = ("ugoira",)


@command()
@option(
    "--speed",
    type=float,
    default=1.0,
    help=(
        "If you want to make animated image file, "
        "you can divide seconds of each frames's interval."
        " Default value is 1.0 (no change)"
    ),
)
@option(
    "--format",
    "-f",
    type=str,
    default="gif",
    help=(
        "Format of result file."
        " You can select apng, gif, webp, and zip format."
        " Default value is gif."
    ),
)
@option(
    "--dest",
    "-d",
    type=ClickPath(),
    default="{}.{}",
    help=(
        "A format string specifying the path of downloaded files."
        " The illust ID and your chosen format will replace"
        " {}s in it, if any."
        " Default is './{}.{}'."
    ),
)
@argument("illust-ids", type=int, nargs=-1)
def ugoira(
    speed: float,
    format: str,
    dest: str | None,
    illust_ids: tuple,
):
    """ugoira command to download Pixiv Ugokuillusts."""
    for i, illust_id in enumerate(illust_ids):
        echo(f"Downloading {illust_id} ({i}/{len(illust_ids)})")
        try:
            blob, frames = download_ugoira_zip(illust_id)
        except PixivError as e:
            echo(f"Error: {e}", err=True)
            continue

        path = Path(dest.format(illust_id, format))

        save(format, path, blob, frames, speed)
        echo(
            "Download was completed successfully."
            f" format is {format} and output path is {path!s}",
        )
