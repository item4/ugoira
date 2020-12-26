""":mod:`ugoira.lib` --- Ugoira Download Library
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Ugoira Download Library

"""

import contextlib
import io
import zipfile
from typing import ContextManager, Dict, Tuple

from PIL import Image

from fake_useragent import UserAgent

from requests import Session


FRAME_DATA_TYPE = Dict[str, int]

#: (:class:`requests.Session`) requests Session for keep headers
pixiv = Session()
pixiv.headers['User-Agent'] = UserAgent().chrome


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


def get_metadata_url(illust_id: int) -> str:
    """Get illust Metadata URL from ``illust_id``.

    :param illust_id: Pixiv illust_id
    :type illust_id: :class:`int`
    :return: Pixiv Metadata URL
    :rtype: :class:`str`

    """
    return (
        'https://www.pixiv.net/ajax/illust/'
        '{}/ugoira_meta'.format(illust_id)
    )


def download_ugoira_zip(illust_id: int) -> Tuple[bytes, FRAME_DATA_TYPE]:
    """Download ugoira zip archive.

    :param illust_id: Pixiv illust_id
    :type illust_id: :class:`int`
    :return: blob of zip file and frame data
    :raise PixivError: If fail to access to image file.

    """

    url = get_metadata_url(illust_id)
    data = pixiv.get(url).json()
    if data['error']:
        raise PixivError('Illust ID {} is not ugoira.'.format(illust_id))
    pixiv.headers['Referer'] = get_illust_url(illust_id)
    body = data['body']
    for key, raising in [['originalSrc', False], ['src', True]]:
        try:
            src = body[key]
        except KeyError:
            continue
        resp = pixiv.head(src)
        if resp.status_code != 200:
            if raising:
                raise PixivError(
                    'Wrong image src. Please report it with illust-id',
                )
            continue
        resp = pixiv.get(src)
        if resp.status_code != 200:
            if raising:
                raise PixivError('Can not download image zip')
            continue
        frames = {f['file']: f['delay'] for f in body['frames']}
        return resp.content, frames
    raise PixivError('Can not download it. Please report it with illust-id')


@contextlib.contextmanager
def open_zip_blob(blob: bytes) -> ContextManager[zipfile.ZipFile]:
    """Make temporary zip file and open it for touch inner files

    :param blob: blob of zip file from :func:`ugoira.lib.download_ugoira_zip`
    :type blob: :class:`bytes`

    """

    assert isinstance(blob, (bytes, bytearray)), "Parameter `blob` must be " \
        "of types (bytes, bytearray). Passed %s (%s)" % (type(blob), blob)

    f = io.BytesIO(blob)
    with zipfile.ZipFile(f) as zf:
        yield zf


def convert_apng(
    blob: bytes,
    frames: FRAME_DATA_TYPE,
    speed: float = 1.0,
):
    """Make APNG file from given file data and frame data.

    This function must need apng library dependency.

    :param blob: blob of zip file from :func:`ugoira.lib.download_ugoira_zip`
    :type blob: :class:`bytes`
    :param frames: mapping object of each frame's filename and interval
    :param speed: frame interval control value
    :type speed: :class:`float`

    :return: Binary string containing generated APNG file

    """

    from apng import APNG, PNG

    with open_zip_blob(blob) as zf:
        files = zf.namelist()
        container = APNG()

        for file in files:
            f = io.BytesIO(zf.read(file))
            container.append(
                PNG.open_any(f),
                delay=int(frames[file]//speed),
            )

        return container.to_bytes()


def make_apng(
    dest: str,
    blob: bytes,
    frames: FRAME_DATA_TYPE,
    speed: float = 1.0,
    *args,
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

    apng_bytes = convert_apng(blob, frames, speed)
    with open(dest, "wb") as fp:
        fp.write(apng_bytes)


def make_via_pillow(
    dest: str,
    blob: bytes,
    frames: FRAME_DATA_TYPE,
    speed: float = 1.0,
    format: str = 'gif',
):
    """Make animated file from given file data and frame data.

    :param dest: path of output file
    :type dest: :class:`str`
    :param blob: blob of zip file from :func:`ugoira.lib.download_ugoira_zip`
    :type blob: :class:`bytes`
    :param frames: mapping object of each frame's filename and interval
    :param speed: frame interval control value
    :type speed: :class:`float`
    :param format: format of result file
    :type format: :class:`str`

    """

    with open_zip_blob(blob) as zf:
        files = zf.namelist()
        images = []
        durations = []
        width = 0
        height = 0
        for file in files:
            f = io.BytesIO(zf.read(file))
            im = Image.open(fp=f)
            width = max(im.width, width)
            height = max(im.height, height)
            images.append(im)
            if format == 'gif':
                durations.append(frames[file]//10//speed)
            elif format == 'webp':
                durations.append(int(frames[file] / speed))

        first_im = images.pop(0)
        kwargs = {
            'format': format,
            'save_all': True,
            'append_images': images,
        }
        if format == 'gif':
            kwargs['duration'] = durations
            kwargs['loop'] = 0
        elif format == 'webp':
            kwargs['duration'] = durations
            kwargs['lossless'] = True
            kwargs['quality'] = 100
            kwargs['method'] = 6

        first_im.save(dest, **kwargs)


def make_zip(
    dest: str,
    blob: bytes,
    *args,
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
    speed: float = 1.0,
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
        'gif': make_via_pillow,
        'pdf': make_via_pillow,
        'webp': make_via_pillow,
    }.get(format)(dest, blob, frames, speed, format)
