""":mod:`ugoira.lib` --- Ugoira Download Library
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Ugoira Download Library

"""

import contextlib
import io
import sys
import zipfile
from pathlib import Path

import httpx
from PIL import Image
from fake_useragent import UserAgent

FrameData = dict[str, int]
HTTP_OK = 200

#: (:class:`httpx.Client`) httpx Client for keep headers
pixiv = httpx.Client(
    headers={
        "User-Agent": UserAgent().chrome,
    },
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
    return f"https://www.pixiv.net/artworks/{illust_id}"


def get_metadata_url(illust_id: int) -> str:
    """Get illust Metadata URL from ``illust_id``.

    :param illust_id: Pixiv illust_id
    :type illust_id: :class:`int`
    :return: Pixiv Metadata URL
    :rtype: :class:`str`

    """
    return f"https://www.pixiv.net/ajax/illust/{illust_id}/ugoira_meta"


def download_ugoira_zip(illust_id: int) -> tuple[bytes, FrameData]:
    """Download ugoira zip archive.

    :param illust_id: Pixiv illust_id
    :type illust_id: :class:`int`
    :return: blob of zip file and frame data
    :raise PixivError: If fail to access to image file.

    """

    url = get_metadata_url(illust_id)
    data = pixiv.get(url).json()
    if data["error"]:
        raise PixivError(f"Illust ID {illust_id} is not ugoira.")
    pixiv.headers["Referer"] = get_illust_url(illust_id)
    body = data["body"]
    for key, raising in [("originalSrc", False), ("src", True)]:
        try:
            src = body[key]
        except KeyError:
            continue
        resp = pixiv.head(src)
        if resp.status_code != HTTP_OK:
            if raising:
                raise PixivError(
                    "Wrong image src. Please report it with illust-id",
                )
            continue
        resp = pixiv.get(src)
        if resp.status_code != HTTP_OK:
            if raising:
                raise PixivError("Can not download image zip")
            continue
        frames = {f["file"]: f["delay"] for f in body["frames"]}
        return resp.content, frames
    raise PixivError("Can not download it. Please report it with illust-id")


@contextlib.contextmanager
def open_zip_blob(blob: bytes) -> zipfile.ZipFile:
    """Make temporary zip file and open it for touch inner files

    :param blob: blob of zip file from :func:`ugoira.lib.download_ugoira_zip`
    :type blob: :class:`bytes`

    """

    if not isinstance(blob, bytes | bytearray):
        print(
            "Parameter `blob` must be of types (bytes, bytearray). Passed"
            f" {type(blob)}",
            file=sys.stderr,
        )
        raise SystemExit(1)

    f = io.BytesIO(blob)
    with zipfile.ZipFile(f) as zf:
        yield zf


def make_via_pillow(
    dest: Path,
    blob: bytes,
    frames: FrameData,
    speed: float = 1.0,
    format: str = "gif",
):
    """Make animated file from given file data and frame data.

    :param dest: path of output file
    :type dest: :class:`Path`
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
            if format == "gif":
                durations.append(frames[file] // speed)
            elif format in {"apng", "webp"}:
                durations.append(int(frames[file] / speed))

        first_im = images.pop(0)
        kwargs = {
            "format": format,
            "save_all": True,
            "append_images": images,
            "duration": durations,
        }
        if format == "gif":
            kwargs["loop"] = 0
        elif format == "webp":
            kwargs["lossless"] = True
            kwargs["quality"] = 100
            kwargs["method"] = 6
        elif format == "apng":
            kwargs["format"] = "png"

        first_im.save(dest, **kwargs)


def make_zip(
    dest: Path,
    blob: bytes,
    *args,
):
    """Make ZIP file from given file data.

    :param dest: path of output file
    :type dest: :class:`Path`
    :param blob: blob of zip file from :func:`ugoira.lib.download_ugoira_zip`
    :type blob: :class:`bytes`

    """

    with dest.open("wb") as f:
        f.write(blob)


def save(
    format: str,
    dest: Path,
    blob: bytes,
    frames: FrameData,
    speed: float = 1.0,
):
    """Save blob to file.

    :param format: file format
    :type format: :class:`str`
    :param dest: path of output file
    :type dest: :class:`Path`
    :param blob: blob of zip file from :func:`ugoira.lib.download_ugoira_zip`
    :type blob: :class:`bytes`
    :param frames: mapping object of each frame's filename and interval
    :param speed: frame interval control value
    :type speed: :class:`float`

    """

    {
        "zip": make_zip,
        "apng": make_via_pillow,
        "gif": make_via_pillow,
        "pdf": make_via_pillow,
        "webp": make_via_pillow,
    }.get(format)(dest, blob, frames, speed, format)
