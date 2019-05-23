""":mod:`ugoira.lib` --- Ugoira Download Library
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Ugoira Download Library

"""

import contextlib
import json
import pathlib
import re
import tempfile
import zipfile
from typing import Dict, Tuple

from fake_useragent import UserAgent

from requests import Session

from wand.image import Image

__all__ = (
    'PixivError',
    'download_ugoira_zip',
    'get_illust_url',
    'is_ugoira',
    'make_apng',
    'make_gif',
    'make_zip',
    'pixiv',
    'save',
    'ugoira_data_regex',
)

FRAME_DATA_TYPE = Dict[str, int]

#: (:class:`requests.Session`) requests Session for keep headers
pixiv = Session()
pixiv.headers['User-Agent'] = UserAgent().chrome

#: (:class:`re.regex`) regular expression for grep ugoira data
ugoira_data_regex = re.compile(
    r'pixiv\.context\.ugokuIllustData\s*=\s*'
    r'(\{"src":".+?","mime_type":".+?","frames":\[.+?\]\})'
)


class PixivError(Exception):
    """Error with Pixiv"""


def get_illust_url(illust_id: int) -> str:
    """Get illust URL from ``illust_id``.

    :param illust_id: Pixiv illust_id
    :type illust_id: :class:`int`
    :return: Pixiv Illust URL
    :rtype: :class:`str`

    """
    return (
        'https://www.pixiv.net/member_illust.php'
        '?mode=medium&illust_id={}'.format(
            illust_id,
        )
    )


def is_ugoira(illust_id: int) -> bool:
    """Check this image type.

    :param illust_id: Pixiv illust_id
    :type illust_id: :class:`int`
    :return: Which is ugoira or not.
    :rtype: :class:`bool`

    """

    res = pixiv.get(get_illust_url(illust_id))
    return '_ugoku-illust-player-container' in res.text


def download_ugoira_zip(illust_id: int) -> Tuple[bytes, FRAME_DATA_TYPE]:
    """Download ugoira zip archive.

    :param illust_id: Pixiv illust_id
    :type illust_id: :class:`int`
    :return: blob of zip file and frame data
    :raise PixivError: If fail to access to image file.

    """

    image_main_url = get_illust_url(illust_id)
    res = pixiv.get(image_main_url)
    data = json.loads(ugoira_data_regex.search(res.text).group(1))
    pixiv.headers['Referer'] = image_main_url
    res = pixiv.head(data['src'])
    if res.status_code != 200:
        raise PixivError('Wrong image src. Please report it with illust-id')
    res = pixiv.get(data['src'])
    if res.status_code != 200:
        raise PixivError('Can not download image zip')
    frames = {f['file']: f['delay'] for f in data['frames']}
    return res.content, frames


@contextlib.contextmanager
def open_zip_blob(blob: bytes):
    """Make temporary zip file and open it for touch inner files

    :param blob: blob of zip file from :func:`ugoira.lib.download_ugoira_zip`
    :type blob: :class:`bytes`

    """

    with tempfile.TemporaryDirectory() as tmpdirname:
        tempzipfile = pathlib.Path(tmpdirname) / 'temp.zip'
        with tempzipfile.open('wb') as f:
            f.write(blob)
        with zipfile.ZipFile(str(tempzipfile)) as zf:
            yield zf


def make_apng(
    dest: str,
    blob: bytes,
    frames: FRAME_DATA_TYPE,
    speed: float=1.0,
):
    """Make APNG file from given file data and frame data.

    This function must need apng library dependency.

    :param dest: path of output file
    :type dest: :class:`str`
    :param blob: blob of zip file from :func:`ugoira.lib.download_ugoira_zip`
    :type blob: :class:`bytes`
    :param frames: mapping object of each frame's filename and interval
    :param speed: frame interval control value
    :type speed: :class:`float`

    """

    from apng import APNG, PNG

    with open_zip_blob(blob) as zf:
        files = zf.namelist()
        container = APNG()

        for fname in files:
            with Image(blob=zf.read(fname)) as frame:
                container.append(
                    PNG.from_bytes(frame.make_blob('png')),
                    delay=int(frames[fname]//speed),
                )

        container.save(dest)


def make_gif(
    dest: str,
    blob: bytes,
    frames: FRAME_DATA_TYPE,
    speed: float=1.0,
):
    """Make GIF file from given file data and frame data.

    :param dest: path of output file
    :type dest: :class:`str`
    :param blob: blob of zip file from :func:`ugoira.lib.download_ugoira_zip`
    :type blob: :class:`bytes`
    :param frames: mapping object of each frame's filename and interval
    :param speed: frame interval control value
    :type speed: :class:`float`

    """

    with open_zip_blob(blob) as zf:
        files = zf.namelist()
        first_image = zf.read(files[0])

        with Image(blob=first_image) as img:
            width = img.width
            height = img.height

        with Image(width=width, height=height) as container:
            container.sequence.clear()  # remove first empty frame
            for fname in files:
                with Image(blob=zf.read(fname)) as orignal_frame:
                    with orignal_frame.convert('gif') as gif_frame:
                        container.sequence.append(gif_frame.sequence[0])
                        with container.sequence[-1]:
                            container.sequence[-1].delay = int(
                                frames[fname]//10//speed
                            )

            container.save(filename=dest)


def make_zip(
    dest: str,
    blob: bytes,
    *args,
    **kwargs
):
    """Make ZIP file from given file data.

    :param dest: path of output file
    :type dest: :class:`str`
    :param blob: blob of zip file from :func:`ugoira.lib.download_ugoira_zip`
    :type blob: :class:`bytes`

    """

    with open(dest, 'wb') as f:
        f.write(blob)


def save(
    format: str,
    dest: str,
    blob: bytes,
    frames: FRAME_DATA_TYPE,
    speed: float=1.0,
):
    """Save blob to file.

    :param format: file format
    :type format: :class:`str`
    :param dest: path of output file
    :type dest: :class:`str`
    :param blob: blob of zip file from :func:`ugoira.lib.download_ugoira_zip`
    :type blob: :class:`bytes`
    :param frames: mapping object of each frame's filename and interval
    :param speed: frame interval control value
    :type speed: :class:`float`

    """

    {
        'zip': make_zip,
        'apng': make_apng,
        'gif': make_gif,
    }.get(format)(dest, blob, frames, speed)
