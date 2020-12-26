import mimetypes
import zipfile

from PIL import Image

from apng import APNG

import pytest

import responses

from ugoira.lib import (
    PixivError,
    download_ugoira_zip,
    get_metadata_url,
    make_apng,
    make_via_pillow,
    make_zip,
)


def test_download_ugoira_wrong_illust_id(
    ugoira_id,
    error_meta_body,
):
    """Test :func:`ugoira.lib.download_ugoira_zip` with wrong illust-id.

    It must raise :class:`ugoira.lib.PixivError`.

    """

    @responses.activate
    def test():
        responses.reset()
        responses.add(**{
            'method': responses.GET,
            'url': get_metadata_url(ugoira_id),
            'body': error_meta_body,
            'content_type': 'application/json',
            'status': 200,
            'match_querystring': True,
        })

        with pytest.raises(PixivError):
            download_ugoira_zip(ugoira_id)

    test()


def test_download_ugoira_zip_fail_head(
    ugoira_id,
    meta_body,
    small_zip_url,
    big_zip_url,
):
    """Test :func:`ugoira.lib.download_ugoira_zip` with broken link.

    It must raise :class:`ugoira.lib.PixivError`.

    """

    @responses.activate
    def case1():
        """
        original head - bad
        original get - not reached
        common head - bad
        common get - not reached
        """
        responses.reset()
        responses.add(**{
            'method': responses.GET,
            'url': get_metadata_url(ugoira_id),
            'body': meta_body,
            'content_type': 'application/json',
            'status': 200,
            'match_querystring': True,
        })
        responses.add(**{
            'method': responses.HEAD,
            'url': big_zip_url,
            'status': 403,
        })
        responses.add(**{
            'method': responses.HEAD,
            'url': small_zip_url,
            'status': 403,
        })

        with pytest.raises(PixivError):
            download_ugoira_zip(ugoira_id)

    @responses.activate
    def case2():
        """
        original head - good
        original get - bad
        common head - bad
        common get - not reached
        """
        responses.reset()
        responses.add(**{
            'method': responses.GET,
            'url': get_metadata_url(ugoira_id),
            'body': meta_body,
            'content_type': 'application/json',
            'status': 200,
            'match_querystring': True,
        })
        responses.add(**{
            'method': responses.HEAD,
            'url': big_zip_url,
            'status': 200,
        })
        responses.add(**{
            'method': responses.GET,
            'url': big_zip_url,
            'status': 403,
        })
        responses.add(**{
            'method': responses.HEAD,
            'url': small_zip_url,
            'status': 403,
        })

        with pytest.raises(PixivError):
            download_ugoira_zip(ugoira_id)

    case1()
    case2()


def test_download_ugoira_zip_fail_get(
    ugoira_id,
    meta_body,
    small_zip_url,
    big_zip_url,
):
    """Test :func:`ugoira.lib.download_ugoira_zip` with broken link.

    It must raise :class:`ugoira.lib.PixivError`.

    """

    @responses.activate
    def case1():
        """
        original head - bad
        original get - not reached
        common head - good
        common get - bad
        """

        responses.reset()
        responses.add(**{
            'method': responses.GET,
            'url': get_metadata_url(ugoira_id),
            'body': meta_body,
            'content_type': 'application/json',
            'status': 200,
            'match_querystring': True,
        })
        responses.add(**{
            'method': responses.HEAD,
            'url': big_zip_url,
            'status': 403,
        })
        responses.add(**{
            'method': responses.HEAD,
            'url': small_zip_url,
            'status': 200,
        })
        responses.add(**{
            'method': responses.GET,
            'url': small_zip_url,
            'status': 403,
        })

        with pytest.raises(PixivError):
            download_ugoira_zip(ugoira_id)

    @responses.activate
    def case2():
        """
        original head - good
        original get - bad
        common head - good
        common get - bad
        """

        responses.reset()
        responses.add(**{
            'method': responses.GET,
            'url': get_metadata_url(ugoira_id),
            'body': meta_body,
            'content_type': 'application/json',
            'status': 200,
            'match_querystring': True,
        })
        responses.add(**{
            'method': responses.HEAD,
            'url': big_zip_url,
            'status': 200,
        })
        responses.add(**{
            'method': responses.GET,
            'url': big_zip_url,
            'status': 403,
        })
        responses.add(**{
            'method': responses.HEAD,
            'url': small_zip_url,
            'status': 200,
        })
        responses.add(**{
            'method': responses.GET,
            'url': small_zip_url,
            'status': 403,
        })

        with pytest.raises(PixivError):
            download_ugoira_zip(ugoira_id)

    case1()
    case2()


def test_download_ugoira_zip_success(
    ugoira_id,
    meta_body,
    small_zip_url,
    big_zip_url,
    small_image_zip,
    big_image_zip,
):
    """Test :func:`ugoira.lib.download_ugoira_zip` with correct link."""

    @responses.activate
    def case1():
        """
        original head - good
        original get - good
        common head - not reached
        common get - not reached
        """
        responses.reset()
        responses.add(**{
            'method': responses.GET,
            'url': get_metadata_url(ugoira_id),
            'body': meta_body,
            'content_type': 'application/json',
            'status': 200,
            'match_querystring': True,
        })
        responses.add(**{
            'method': responses.HEAD,
            'url': big_zip_url,
            'status': 200,
        })
        responses.add(**{
            'method': responses.GET,
            'url': big_zip_url,
            'body': big_image_zip,
            'content_type': 'application/zip',
            'status': 200,
        })

        data, frames = download_ugoira_zip(ugoira_id)
        assert data == big_image_zip

    @responses.activate
    def case2():
        """
        original head - good
        original get - bad
        common head - good
        common get - good
        """
        responses.reset()
        responses.add(**{
            'method': responses.GET,
            'url': get_metadata_url(ugoira_id),
            'body': meta_body,
            'content_type': 'application/json',
            'status': 200,
            'match_querystring': True,
        })
        responses.add(**{
            'method': responses.HEAD,
            'url': big_zip_url,
            'status': 200,
        })
        responses.add(**{
            'method': responses.GET,
            'url': big_zip_url,
            'status': 403,
        })
        responses.add(**{
            'method': responses.HEAD,
            'url': small_zip_url,
            'status': 200,
        })
        responses.add(**{
            'method': responses.GET,
            'url': small_zip_url,
            'body': small_image_zip,
            'content_type': 'application/zip',
            'status': 200,
        })

        data, frames = download_ugoira_zip(ugoira_id)
        assert data == small_image_zip

    @responses.activate
    def case3():
        """
        original head - bad
        original get - not reached
        common head - good
        common get - good
        """
        responses.reset()
        responses.add(**{
            'method': responses.GET,
            'url': get_metadata_url(ugoira_id),
            'body': meta_body,
            'content_type': 'application/json',
            'status': 200,
            'match_querystring': True,
        })
        responses.add(**{
            'method': responses.HEAD,
            'url': big_zip_url,
            'status': 403,
        })
        responses.add(**{
            'method': responses.HEAD,
            'url': small_zip_url,
            'status': 200,
        })
        responses.add(**{
            'method': responses.GET,
            'url': small_zip_url,
            'body': small_image_zip,
            'content_type': 'application/zip',
            'status': 200,
        })

        data, frames = download_ugoira_zip(ugoira_id)
        assert data == small_image_zip

    case1()
    case2()
    case3()


def test_make_apng(
    fx_tmpdir,
    small_image_zip,
    frames,
):
    """Test :func:`ugoira.lib.make_apng`."""

    dest = str(fx_tmpdir / 'test.apng')
    make_apng(dest, small_image_zip, frames)
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

    dest = str(fx_tmpdir / 'test.gif')
    make_via_pillow(dest, small_image_zip, frames, 1.0, 'gif')
    im = Image.open(dest)

    assert im.format == 'GIF'
    assert im.info['duration'] == 1000 / 10
    assert im.info['loop'] == 0
    im.seek(im.tell() + 1)

    assert im.format == 'GIF'
    assert im.info['duration'] == 2000 / 10
    assert im.info['loop'] == 0
    im.seek(im.tell() + 1)

    assert im.format == 'GIF'
    assert im.info['duration'] == 3000 / 10
    assert im.info['loop'] == 0

    with pytest.raises(EOFError):
        assert im.seek(im.tell() + 1)


def test_make_webp(
    fx_tmpdir,
    small_image_zip,
    frames,
):
    """Test :func:`ugoira.lib.make_gif`."""

    dest = str(fx_tmpdir / 'test.webp')
    make_via_pillow(dest, small_image_zip, frames, 1.0, 'webp')
    im = Image.open(dest)
    assert im.format == 'WEBP'
    assert im.info['loop'] == 0


def test_make_pdf(
    fx_tmpdir,
    small_image_zip,
    frames,
):
    """Test :func:`ugoira.lib.make_gif`."""

    dest = str(fx_tmpdir / 'test.pdf')
    make_via_pillow(dest, small_image_zip, frames, 1.0, 'pdf')
    assert mimetypes.guess_type(dest, strict=True) == ('application/pdf', None)


def test_make_zip(
    fx_tmpdir,
    small_image_zip,
    frames,
):
    """Test :func:`ugoira.lib.make_zip` with correct link."""

    dest = str(fx_tmpdir / 'test.zip')

    make_zip(dest, small_image_zip)

    with zipfile.ZipFile(dest) as f:
        assert set(f.namelist()) == set(frames.keys())
