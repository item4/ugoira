""":mod:`ugoira.cli` --- Ugoira Download Command Line
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Ugoira Download Command Line

"""

from .lib import PixivError, download_zip, is_ugoira, login, make_gif, save_zip

from click import Path, argument, command, echo, option


__all__ = 'ugoira',


@command()
@option('--id', prompt='Your Pixiv ID', help='Pixiv ID')
@option('--password', prompt=True, hide_input=True, help='Pixiv Password')
@option('--div-by', type=int, default=1, help='You can divide interval between'
                                              ' images by using this option.'
                                              ' Default value is 1'
                                              ' (normal speed)')
@argument('image-id', type=int)
@argument('dest', type=Path())
def ugoira(id: str, password: str, div_by: int, image_id: int, dest: str):
    """ugoira command for download Pixiv Ugokuillust."""

    try:
        if login(id, password):
            pass
        else:
            echo('Login failed.', err=True)
            raise SystemExit(1)
    except PixivError as e:
        echo(e, err=True)
        raise SystemExit(1)
    if is_ugoira(image_id):
        blob, frames = download_zip(image_id)
        if dest.endswith('.zip'):
            save_zip(dest, blob)
            echo('download completed at {} as zip'.format(dest))
        else:
            if not dest.endswith('.gif'):
                dest += '.gif'

            make_gif(dest, blob, frames, div_by)
            echo('download completed at {} as gif'.format(dest))
    else:
        echo('Given image id is not ugoira.', err=True)
        raise SystemExit(1)
