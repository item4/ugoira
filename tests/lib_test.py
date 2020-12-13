import zipfile

from apng import APNG

import pytest

import responses

from ugoira.lib import (
    PixivError,
    download_ugoira_zip,
    get_metadata_url,
    make_apng,
    make_gif,
    make_zip,
)

from wand.image import Image

ugoira_id = 74442143
non_ugoira_id = 74073488
zip_url = 'https://i.pximg.net/img-zip-ugoira/img/' \
          '2019/04/29/16/09/38/74442143_ugoira600x600.zip'
big_zip_url = 'https://i.pximg.net/img-zip-ugoira/img/' \
              '2019/04/29/16/09/38/74442143_ugoira1920x1080.zip'


def test_download_ugoira_wrong_illust_id(fx_non_ugoira_body):
    """Test :func:`ugoira.lib.download_ugoira_zip` with wrong illust-id.

    It must raise :class:`ugoira.lib.PixivError`.

    """

    @responses.activate
    def test():
        responses.reset()
        responses.add(**{
            'method': responses.GET,
            'url': get_metadata_url(ugoira_id),
            'body': fx_non_ugoira_body,
            'content_type': 'application/json',
            'status': 200,
            'match_querystring': True,
        })

        with pytest.raises(PixivError):
            download_ugoira_zip(ugoira_id)

    test()


def test_download_ugoira_zip_fail_head(fx_ugoira_body):
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
            'body': fx_ugoira_body,
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
            'url': zip_url,
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
            'body': fx_ugoira_body,
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
            'url': zip_url,
            'status': 403,
        })

        with pytest.raises(PixivError):
            download_ugoira_zip(ugoira_id)

    case1()
    case2()


def test_download_ugoira_zip_fail_get(fx_ugoira_body):
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
            'body': fx_ugoira_body,
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
            'url': zip_url,
            'status': 200,
        })
        responses.add(**{
            'method': responses.GET,
            'url': zip_url,
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
            'body': fx_ugoira_body,
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
            'url': zip_url,
            'status': 200,
        })
        responses.add(**{
            'method': responses.GET,
            'url': zip_url,
            'status': 403,
        })

        with pytest.raises(PixivError):
            download_ugoira_zip(ugoira_id)

    case1()
    case2()


def test_download_ugoira_zip_success(
    fx_ugoira_body,
    fx_ugoira_zip,
    fx_ugoira_big_zip,
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
            'body': fx_ugoira_body,
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
            'body': fx_ugoira_big_zip,
            'content_type': 'application/zip',
            'status': 200,
        })

        data, frames = download_ugoira_zip(ugoira_id)
        assert data == fx_ugoira_big_zip

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
            'body': fx_ugoira_body,
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
            'url': zip_url,
            'status': 200,
        })
        responses.add(**{
            'method': responses.GET,
            'url': zip_url,
            'body': fx_ugoira_zip,
            'content_type': 'application/zip',
            'status': 200,
        })

        data, frames = download_ugoira_zip(ugoira_id)
        assert data == fx_ugoira_zip

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
            'body': fx_ugoira_body,
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
            'url': zip_url,
            'status': 200,
        })
        responses.add(**{
            'method': responses.GET,
            'url': zip_url,
            'body': fx_ugoira_zip,
            'content_type': 'application/zip',
            'status': 200,
        })

        data, frames = download_ugoira_zip(ugoira_id)
        assert data == fx_ugoira_zip

    case1()


def test_make_apng(
    fx_tmpdir,
    fx_ugoira_zip,
    fx_ugoira_frames,
):
    """Test :func:`ugoira.lib.make_apng`."""

    dest = str(fx_tmpdir / 'test.apng')
    make_apng(dest, fx_ugoira_zip, fx_ugoira_frames)
    img = APNG.open(dest)

    assert len(img.frames) == 3
    assert img.frames[0][1].delay == 1000
    assert img.frames[1][1].delay == 2000
    assert img.frames[2][1].delay == 3000


def test_make_gif(
    fx_tmpdir,
    fx_ugoira_zip,
    fx_ugoira_frames,
):
    """Test :func:`ugoira.lib.make_gif`."""

    dest = str(fx_tmpdir / 'test.gif')
    make_gif(dest, fx_ugoira_zip, fx_ugoira_frames)
    with Image(filename=dest) as img:
        assert img.format == 'GIF'
        assert len(img.sequence) == 3
        assert img.sequence[0].delay == 100
        assert img.sequence[1].delay == 200
        assert img.sequence[2].delay == 300


def test_make_zip(
    fx_tmpdir,
    fx_ugoira_zip,
    fx_ugoira_frames,
):
    """Test :func:`ugoira.lib.make_zip` with correct link."""

    dest = str(fx_tmpdir / 'test.zip')

    make_zip(dest, fx_ugoira_zip)

    with zipfile.ZipFile(dest) as f:
        assert set(f.namelist()) == set(fx_ugoira_frames.keys())
