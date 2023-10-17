import mimetypes
import zipfile

import pytest
from PIL import Image
from apng import APNG

from ugoira.lib import PixivError
from ugoira.lib import download_ugoira_zip
from ugoira.lib import get_metadata_url
from ugoira.lib import make_via_pillow
from ugoira.lib import make_zip


def test_download_ugoira_wrong_illust_id(
    ugoira_id,
    error_meta_body,
    httpx_mock,
):
    """Test :func:`ugoira.lib.download_ugoira_zip` with wrong illust-id.

    It must raise :class:`ugoira.lib.PixivError`.

    """

    httpx_mock.add_response(
        method="GET",
        url=get_metadata_url(ugoira_id),
        json=error_meta_body,
        status_code=200,
    )

    with pytest.raises(PixivError):
        download_ugoira_zip(ugoira_id)


def test_download_ugoira_zip_fail_head_case1(
    ugoira_id,
    meta_body,
    small_zip_url,
    big_zip_url,
    httpx_mock,
):
    """Test :func:`ugoira.lib.download_ugoira_zip` with broken link.

    It must raise :class:`ugoira.lib.PixivError`.

    original head - bad
    original get - not reached
    common head - bad
    common get - not reached
    """
    httpx_mock.add_response(
        method="GET",
        url=get_metadata_url(ugoira_id),
        json=meta_body,
        status_code=200,
    )
    httpx_mock.add_response(
        method="HEAD",
        url=big_zip_url,
        status_code=403,
    )
    httpx_mock.add_response(
        method="HEAD",
        url=small_zip_url,
        status_code=403,
    )

    with pytest.raises(PixivError):
        download_ugoira_zip(ugoira_id)


def test_download_ugoira_zip_fail_head_case2(
    ugoira_id,
    meta_body,
    small_zip_url,
    big_zip_url,
    httpx_mock,
):
    """Test :func:`ugoira.lib.download_ugoira_zip` with broken link.

    It must raise :class:`ugoira.lib.PixivError`.
    original head - good
    original get - bad
    common head - bad
    common get - not reached
    """
    httpx_mock.add_response(
        method="GET",
        url=get_metadata_url(ugoira_id),
        json=meta_body,
        status_code=200,
    )
    httpx_mock.add_response(
        method="HEAD",
        url=big_zip_url,
        status_code=200,
    )
    httpx_mock.add_response(
        method="GET",
        url=big_zip_url,
        status_code=403,
    )
    httpx_mock.add_response(
        method="HEAD",
        url=small_zip_url,
        status_code=403,
    )

    with pytest.raises(PixivError):
        download_ugoira_zip(ugoira_id)


def test_download_ugoira_zip_fail_get_case2(
    ugoira_id,
    meta_body,
    small_zip_url,
    big_zip_url,
    httpx_mock,
):
    """Test :func:`ugoira.lib.download_ugoira_zip` with broken link.

    It must raise :class:`ugoira.lib.PixivError`.

    original head - bad
    original get - not reached
    common head - good
    common get - bad
    """
    httpx_mock.add_response(
        method="GET",
        url=get_metadata_url(ugoira_id),
        json=meta_body,
        status_code=200,
    )
    httpx_mock.add_response(
        method="HEAD",
        url=big_zip_url,
        status_code=403,
    )
    httpx_mock.add_response(
        method="HEAD",
        url=small_zip_url,
        status_code=200,
    )
    httpx_mock.add_response(
        method="GET",
        url=small_zip_url,
        status_code=403,
    )

    with pytest.raises(PixivError):
        download_ugoira_zip(ugoira_id)


def test_download_ugoira_zip_fail_get_case3(
    ugoira_id,
    meta_body,
    small_zip_url,
    big_zip_url,
    httpx_mock,
):
    """Test :func:`ugoira.lib.download_ugoira_zip` with broken link.

    It must raise :class:`ugoira.lib.PixivError`.

    original head - good
    original get - bad
    common head - good
    common get - bad
    """
    httpx_mock.add_response(
        method="GET",
        url=get_metadata_url(ugoira_id),
        json=meta_body,
        status_code=200,
    )
    httpx_mock.add_response(
        method="HEAD",
        url=big_zip_url,
        status_code=200,
    )
    httpx_mock.add_response(
        method="GET",
        url=big_zip_url,
        status_code=403,
    )
    httpx_mock.add_response(
        method="HEAD",
        url=small_zip_url,
        status_code=200,
    )
    httpx_mock.add_response(
        method="GET",
        url=small_zip_url,
        status_code=403,
    )

    with pytest.raises(PixivError):
        download_ugoira_zip(ugoira_id)


def test_download_ugoira_zip_success_case1(
    ugoira_id,
    meta_body,
    small_zip_url,
    big_zip_url,
    small_image_zip,
    big_image_zip,
    httpx_mock,
):
    """Test :func:`ugoira.lib.download_ugoira_zip` with correct link.

    original head - good
    original get - good
    common head - not reached
    common get - not reached
    """
    httpx_mock.add_response(
        method="GET",
        url=get_metadata_url(ugoira_id),
        json=meta_body,
        status_code=200,
    )
    httpx_mock.add_response(
        method="HEAD",
        url=big_zip_url,
        status_code=200,
    )
    httpx_mock.add_response(
        method="GET",
        url=big_zip_url,
        content=big_image_zip,
        headers={"content-type": "application/zip"},
        status_code=200,
    )

    data, frames = download_ugoira_zip(ugoira_id)
    assert data == big_image_zip


def test_download_ugoira_zip_success_case2(
    ugoira_id,
    meta_body,
    small_zip_url,
    big_zip_url,
    small_image_zip,
    big_image_zip,
    httpx_mock,
):
    """Test :func:`ugoira.lib.download_ugoira_zip` with correct link.

    original head - good
    original get - bad
    common head - good
    common get - good
    """
    httpx_mock.add_response(
        method="GET",
        url=get_metadata_url(ugoira_id),
        json=meta_body,
        status_code=200,
    )
    httpx_mock.add_response(
        method="HEAD",
        url=big_zip_url,
        status_code=200,
    )
    httpx_mock.add_response(
        method="GET",
        url=big_zip_url,
        status_code=403,
    )
    httpx_mock.add_response(
        method="HEAD",
        url=small_zip_url,
        status_code=200,
    )
    httpx_mock.add_response(
        method="GET",
        url=small_zip_url,
        content=small_image_zip,
        headers={"content-type": "application/zip"},
        status_code=200,
    )

    data, frames = download_ugoira_zip(ugoira_id)
    assert data == small_image_zip


def test_download_ugoira_zip_success_case3(
    ugoira_id,
    meta_body,
    small_zip_url,
    big_zip_url,
    small_image_zip,
    big_image_zip,
    httpx_mock,
):
    """Test :func:`ugoira.lib.download_ugoira_zip` with correct link.

    original head - bad
    original get - not reached
    common head - good
    common get - good
    """
    httpx_mock.add_response(
        method="GET",
        url=get_metadata_url(ugoira_id),
        json=meta_body,
        status_code=200,
    )
    httpx_mock.add_response(
        method="HEAD",
        url=big_zip_url,
        status_code=403,
    )
    httpx_mock.add_response(
        method="HEAD",
        url=small_zip_url,
        status_code=200,
    )
    httpx_mock.add_response(
        method="GET",
        url=small_zip_url,
        content=small_image_zip,
        headers={"content-type": "application/zip"},
        status_code=200,
    )

    data, frames = download_ugoira_zip(ugoira_id)
    assert data == small_image_zip


def test_make_apng(
    fx_tmpdir,
    small_image_zip,
    frames,
):
    """Test :func:`ugoira.lib.make_apng`."""

    dest = fx_tmpdir / "test.apng"
    make_via_pillow(dest, small_image_zip, frames, format="apng")
    img = APNG.open(dest)

    assert len(img.frames) == 3
    assert img.frames[0][1].delay == 1000
    assert img.frames[1][1].delay == 2000
    assert img.frames[2][1].delay == 3000


def test_make_gif(
    fx_tmpdir,
    small_image_zip,
    frames,
):
    """Test :func:`ugoira.lib.make_gif`."""

    dest = fx_tmpdir / "test.gif"
    make_via_pillow(dest, small_image_zip, frames, 1.0, "gif")
    im = Image.open(dest)

    assert im.format == "GIF"
    assert im.info["duration"] == 1000
    assert im.info["loop"] == 0
    im.seek(im.tell() + 1)

    assert im.format == "GIF"
    assert im.info["duration"] == 2000
    assert im.info["loop"] == 0
    im.seek(im.tell() + 1)

    assert im.format == "GIF"
    assert im.info["duration"] == 3000
    assert im.info["loop"] == 0

    with pytest.raises(EOFError):
        assert im.seek(im.tell() + 1)


def test_make_webp(
    fx_tmpdir,
    small_image_zip,
    frames,
):
    """Test :func:`ugoira.lib.make_gif`."""

    dest = fx_tmpdir / "test.webp"
    make_via_pillow(dest, small_image_zip, frames, 1.0, "webp")
    im = Image.open(dest)
    assert im.format == "WEBP"
    assert im.info["loop"] == 0


def test_make_pdf(
    fx_tmpdir,
    small_image_zip,
    frames,
):
    """Test :func:`ugoira.lib.make_gif`."""

    dest = fx_tmpdir / "test.pdf"
    make_via_pillow(dest, small_image_zip, frames, 1.0, "pdf")
    assert mimetypes.guess_type(dest, strict=True) == ("application/pdf", None)


def test_make_zip(
    fx_tmpdir,
    small_image_zip,
    frames,
):
    """Test :func:`ugoira.lib.make_zip` with correct link."""

    dest = fx_tmpdir / "test.zip"

    make_zip(dest, small_image_zip)

    with zipfile.ZipFile(dest) as f:
        assert set(f.namelist()) == set(frames.keys())
