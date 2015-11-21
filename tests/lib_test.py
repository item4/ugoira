import contextlib
import zipfile

import pytest
import responses
from ugoira.lib import (PixivError, download_zip, is_ugoira, login, make_gif,
                        save_zip)
from wand.image import Image


def test_login_valid(fx_valid_id_pw):
    """Test :func:`ugoira.lib.login` successfully.

    """

    @responses.activate
    def test():
        responses.reset()
        responses.add(**{
            'method': responses.GET,
            'url': 'http://www.pixiv.net/',
            'body': 'Just touch, Do not access it really.'
                    ' Because they block us.',
            'content_type': 'text/html; charset=utf-8',
            'status': 200,
        })
        responses.add(**{
            'method': responses.POST,
            'url': 'https://www.secure.pixiv.net/login.php',
            'body': 'Just touch, Do not access it really.'
                    ' Because they block us.',
            'content_type': 'text/html; charset=utf-8',
            'status': 301,
            'adding_headers': {
                'Location': 'http://www.pixiv.net/'
            },
        })

        assert login(*fx_valid_id_pw)

    test()


def test_login_pw_is_too_short(fx_too_short_id_pw):
    """Test :func:`ugoira.lib.login` with too short password.

    It must raise :class:`ugoira.lib.PixivError`.

    """

    @responses.activate
    def test():
        responses.reset()
        responses.add(**{
            'method': responses.GET,
            'url': 'http://www.pixiv.net/',
            'body': 'Just touch, Do not access it really.'
                    ' Because they block us.',
            'content_type': 'text/html; charset=utf-8',
            'status': 200,
        })
        with pytest.raises(PixivError):
            login(*fx_too_short_id_pw)

    test()


def test_login_pw_is_too_long(fx_too_long_id_pw):
    """Test :func:`ugoira.lib.login` with too long password.

    It must raise :class:`ugoira.lib.PixivError`.

    """

    @responses.activate
    def test():
        responses.reset()
        responses.add(**{
            'method': responses.GET,
            'url': 'http://www.pixiv.net/',
            'body': 'Just touch, Do not access it really.'
                    ' Because they block us.',
            'content_type': 'text/html; charset=utf-8',
            'status': 200,
        })
        with pytest.raises(PixivError):
            login(*fx_too_long_id_pw)

    test()


def test_login_invalid(fx_invalid_id_pw):
    """Test :func:`ugoira.lib.login` with invalid id/pw pair.

    It must raise :class:`ugoira.lib.PixivError`.

    """

    @responses.activate
    def test():
        responses.reset()
        responses.add(**{
            'method': responses.GET,
            'url': 'http://www.pixiv.net/',
            'body': 'Just touch, Do not access it really.'
                    ' Because they block us.',
            'content_type': 'text/html; charset=utf-8',
            'status': 200,
        })
        responses.add(**{
            'method': responses.POST,
            'url': 'https://www.secure.pixiv.net/login.php',
            'body': 'Just touch, Do not access it really.'
                    ' Because they block us.',
            'content_type': 'text/html; charset=utf-8',
            'status': 301,
            'adding_headers': {
                'Location': 'http://example.com/'
            },
        })
        responses.add(**{
            'method': responses.GET,
            'url': 'http://example.com/',
            'body': 'Just touch, Do not access it really.'
                    ' Because they block us.',
            'content_type': 'text/html; charset=utf-8',
            'status': 200,
        })

        assert not login(*fx_invalid_id_pw)

    test()


def test_login_too_many_fail(fx_invalid_id_pw):
    """Test :func:`ugoira.lib.login` with too many fail before.

    It must raise :class:`ugoira.lib.PixivError`.

    """

    @responses.activate
    def test():
        responses.reset()
        responses.add(**{
            'method': responses.GET,
            'url': 'http://www.pixiv.net/',
            'body': 'Just touch, Do not access it really.'
                    ' Because they block us.',
            'content_type': 'text/html; charset=utf-8',
            'status': 200,
        })
        responses.add(**{
            'method': responses.POST,
            'url': 'https://www.secure.pixiv.net/login.php',
            'body': '誤入力が続いたため、アカウントのロックを行いました。'
                    'しばらく経ってからログインをお試しください。',
            'content_type': 'text/html; charset=utf-8',
            'status': 200,
        })

        with pytest.raises(PixivError):
            login(*fx_invalid_id_pw)

    test()


def test_is_ugoira_true(fx_ugoira_body):
    """Test :func:`ugoira.lib.ugoira`.

    Result is :const:`True`.

    """

    @responses.activate
    def test():
        responses.reset()
        responses.add(**{
            'method': responses.GET,
            'url': 'http://www.pixiv.net/member_illust.php'
                   '?mode=medium&illust_id=53239740',
            'body': fx_ugoira_body,
            'content_type': 'text/html; charset=utf-8',
            'status': 200,
            'match_querystring': True,
        })

        assert is_ugoira(53239740)

    test()


def test_is_ugoira_false(fx_non_ugoira_body):
    """Test :func:`ugoira.lib.ugoira`.

    Result is :const:`False`.

    """

    @responses.activate
    def test():
        responses.reset()
        responses.add(**{
            'method': responses.GET,
            'url': 'http://www.pixiv.net/member_illust.php'
                   '?mode=medium&illust_id=53231212',
            'body': fx_non_ugoira_body,
            'content_type': 'text/html; charset=utf-8',
            'status': 200,
            'match_querystring': True,
        })

        assert not is_ugoira(53231212)

    test()


def test_download_zip_fail_head(fx_ugoira_body):
    """Test :func:`ugoira.lib.download_zip` with broken link.

    It must raise :class:`ugoira.lib.PixivError`.

    """

    @responses.activate
    def test():
        responses.reset()
        responses.add(**{
            'method': responses.GET,
            'url': 'http://www.pixiv.net/member_illust.php'
                   '?mode=medium&illust_id=53239740',
            'body': fx_ugoira_body,
            'content_type': 'text/html; charset=utf-8',
            'status': 200,
            'match_querystring': True,
        })
        responses.add(**{
            'method': responses.HEAD,
            'url': 'http://i1.pixiv.net/img-zip-ugoira/img/'
                   '2015/10/27/22/10/14/53239740_ugoira600x600.zip',
            'status': 403,
        })

        with pytest.raises(PixivError):
            download_zip(53239740)

    test()


def test_download_zip_fail_get(fx_ugoira_body):
    """Test :func:`ugoira.lib.download_zip` with broken link.

    It must raise :class:`ugoira.lib.PixivError`.

    """

    @responses.activate
    def test():
        responses.reset()
        responses.add(**{
            'method': responses.GET,
            'url': 'http://www.pixiv.net/member_illust.php'
                   '?mode=medium&illust_id=53239740',
            'body': fx_ugoira_body,
            'content_type': 'text/html; charset=utf-8',
            'status': 200,
            'match_querystring': True,
        })
        responses.add(**{
            'method': responses.HEAD,
            'url': 'http://i1.pixiv.net/img-zip-ugoira/img/'
                   '2015/10/27/22/10/14/53239740_ugoira600x600.zip',
            'status': 200,
        })
        responses.add(**{
            'method': responses.GET,
            'url': 'http://i1.pixiv.net/img-zip-ugoira/img/'
                   '2015/10/27/22/10/14/53239740_ugoira600x600.zip',
            'status': 403,
        })

        with pytest.raises(PixivError):
            download_zip(53239740)

    test()


def test_download_zip_success(fx_ugoira_body, fx_ugoira_zip):
    """Test :func:`ugoira.lib.download_zip` with correct link."""

    @responses.activate
    def test():
        responses.reset()
        responses.add(**{
            'method': responses.GET,
            'url': 'http://www.pixiv.net/member_illust.php'
                   '?mode=medium&illust_id=53239740',
            'body': fx_ugoira_body,
            'content_type': 'text/html; charset=utf-8',
            'status': 200,
            'match_querystring': True,
        })
        responses.add(**{
            'method': responses.HEAD,
            'url': 'http://i1.pixiv.net/img-zip-ugoira/img/'
                   '2015/10/27/22/10/14/53239740_ugoira600x600.zip',
            'status': 200,
        })
        responses.add(**{
            'method': responses.GET,
            'url': 'http://i1.pixiv.net/img-zip-ugoira/img/'
                   '2015/10/27/22/10/14/53239740_ugoira600x600.zip',
            'body': fx_ugoira_zip,
            'content_type': 'application/zip',
            'status': 200,
        })

        data, frames = download_zip(53239740)
        assert data == fx_ugoira_zip

    test()


def test_make_gif(monkeypatch,
                  fx_tmpdir,
                  fx_ugoira_body,
                  fx_ugoira_zip,
                  fx_ugoira_frames):
    """Test :func:`ugoira.lib.make_gif` with correct link."""

    @contextlib.contextmanager
    def fake():
        yield str(fx_tmpdir)
    monkeypatch.setattr('tempfile.TemporaryDirectory', fake)

    @responses.activate
    def test():
        responses.reset()
        responses.add(**{
            'method': responses.GET,
            'url': 'http://www.pixiv.net/member_illust.php'
                   '?mode=medium&illust_id=53239740',
            'body': fx_ugoira_body,
            'content_type': 'text/html; charset=utf-8',
            'status': 200,
            'match_querystring': True,
        })
        responses.add(**{
            'method': responses.HEAD,
            'url': 'http://i1.pixiv.net/img-zip-ugoira/img/'
                   '2015/10/27/22/10/14/53239740_ugoira600x600.zip',
            'status': 200,
        })
        responses.add(**{
            'method': responses.GET,
            'url': 'http://i1.pixiv.net/img-zip-ugoira/img/'
                   '2015/10/27/22/10/14/53239740_ugoira600x600.zip',
            'body': fx_ugoira_zip,
            'content_type': 'application/zip',
            'status': 200,
        })

        data, frames = download_zip(53239740)
        file = fx_tmpdir / 'test.gif'
        make_gif(str(file), data, fx_ugoira_frames)
        with Image(filename=str(file)) as img:
            assert img.format == 'GIF'
            assert len(img.sequence) == 3
            assert img.sequence[0].delay == 100
            assert img.sequence[1].delay == 200
            assert img.sequence[2].delay == 300

    test()


def test_make_gif_with_acceleration(monkeypatch,
                                    fx_tmpdir,
                                    fx_ugoira_body,
                                    fx_ugoira_zip,
                                    fx_ugoira_frames):
    """Test :func:`ugoira.lib.make_gif` with correct link and acceleration."""

    @contextlib.contextmanager
    def fake():
        yield str(fx_tmpdir)
    monkeypatch.setattr('tempfile.TemporaryDirectory', fake)

    @responses.activate
    def test():
        responses.reset()
        responses.add(**{
            'method': responses.GET,
            'url': 'http://www.pixiv.net/member_illust.php'
                   '?mode=medium&illust_id=53239740',
            'body': fx_ugoira_body,
            'content_type': 'text/html; charset=utf-8',
            'status': 200,
            'match_querystring': True,
        })
        responses.add(**{
            'method': responses.HEAD,
            'url': 'http://i1.pixiv.net/img-zip-ugoira/img/'
                   '2015/10/27/22/10/14/53239740_ugoira600x600.zip',
            'status': 200,
        })
        responses.add(**{
            'method': responses.GET,
            'url': 'http://i1.pixiv.net/img-zip-ugoira/img/'
                   '2015/10/27/22/10/14/53239740_ugoira600x600.zip',
            'body': fx_ugoira_zip,
            'content_type': 'application/zip',
            'status': 200,
        })

        data, frames = download_zip(53239740)
        file = fx_tmpdir / 'test.gif'
        make_gif(str(file), data, fx_ugoira_frames, 10.0)
        with Image(filename=str(file)) as img:
            assert img.format == 'GIF'
            assert len(img.sequence) == 3
            assert img.sequence[0].delay == 10
            assert img.sequence[1].delay == 20
            assert img.sequence[2].delay == 30

    test()


def test_save_zip(monkeypatch,
                  fx_tmpdir,
                  fx_ugoira_body,
                  fx_ugoira_zip,
                  fx_ugoira_frames):
    """Test :func:`ugoira.lib.save_zip` with correct link."""

    @contextlib.contextmanager
    def fake():
        yield str(fx_tmpdir)
    monkeypatch.setattr('tempfile.TemporaryDirectory', fake)

    @responses.activate
    def test():
        responses.reset()
        responses.add(**{
            'method': responses.GET,
            'url': 'http://www.pixiv.net/member_illust.php'
                   '?mode=medium&illust_id=53239740',
            'body': fx_ugoira_body,
            'content_type': 'text/html; charset=utf-8',
            'status': 200,
            'match_querystring': True,
        })
        responses.add(**{
            'method': responses.HEAD,
            'url': 'http://i1.pixiv.net/img-zip-ugoira/img/'
                   '2015/10/27/22/10/14/53239740_ugoira600x600.zip',
            'status': 200,
        })
        responses.add(**{
            'method': responses.GET,
            'url': 'http://i1.pixiv.net/img-zip-ugoira/img/'
                   '2015/10/27/22/10/14/53239740_ugoira600x600.zip',
            'body': fx_ugoira_zip,
            'content_type': 'application/zip',
            'status': 200,
        })

        data, frames = download_zip(53239740)
        file = fx_tmpdir / 'test.zip'

        save_zip(str(file), data)

        with zipfile.ZipFile(str(file)) as f:
            namelist = f.namelist()
            assert len(namelist) == len(fx_ugoira_frames)

            for filename in fx_ugoira_frames.keys():
                assert filename in namelist

    test()
