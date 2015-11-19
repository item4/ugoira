import contextlib
import zipfile

import httpretty
import pytest
from ugoira.lib import (PixivError, download_zip, is_ugoira, login, make_gif,
                        save_zip)
from wand.image import Image

def test_login_valid(fx_valid_id_pw):
    assert login(*fx_valid_id_pw)


def test_login_pw_is_too_short(fx_too_short_id_pw):
    with pytest.raises(PixivError):
        login(*fx_too_short_id_pw)


def test_login_pw_is_too_long(fx_too_long_id_pw):
    with pytest.raises(PixivError):
        login(*fx_too_long_id_pw)


def test_login_invalid(fx_invalid_id_pw):
    with pytest.raises(PixivError):
        login(*fx_invalid_id_pw)


@httpretty.activate
def test_login_too_many_fail(fx_invalid_id_pw):
    httpretty.register_uri(
        httpretty.GET,
        'https://www.secure.pixiv.net/login.php',
        body='ログインの制限を開始しました',
    )

    with pytest.raises(PixivError):
        login(*fx_invalid_id_pw)


@httpretty.activate
def test_is_ugoira(fx_ugoira_body, fx_non_ugoira_body):
    httpretty.register_uri(
        httpretty.GET,
        'http://www.pixiv.net/member_illust.php?mode=medium&illust_id=53239740',
        body=fx_ugoira_body,
    )
    assert is_ugoira(53239740)

    httpretty.register_uri(
        httpretty.GET,
        'http://www.pixiv.net/member_illust.php?mode=medium&illust_id=53231212',
        body=fx_non_ugoira_body,
    )
    assert not is_ugoira(53231212)


@httpretty.activate
def test_download_zip_fail_head(fx_ugoira_body, fx_ugoira_zip):
    httpretty.register_uri(
        httpretty.GET,
        'http://www.pixiv.net/member_illust.php?mode=medium&illust_id=53239740',
        body=fx_ugoira_body,
    )
    httpretty.register_uri(
        httpretty.HEAD,
        'http://i1.pixiv.net/img-zip-ugoira/img/2015/10/27/22/10/14/53239740_ugoira600x600.zip',
        status=403,
    )

    with pytest.raises(PixivError):
        download_zip(53239740)


@httpretty.activate
def test_download_zip_fail_get(fx_ugoira_body, fx_ugoira_zip):
    httpretty.register_uri(
        httpretty.GET,
        'http://www.pixiv.net/member_illust.php?mode=medium&illust_id=53239740',
        body=fx_ugoira_body,
    )
    httpretty.register_uri(
        httpretty.HEAD,
        'http://i1.pixiv.net/img-zip-ugoira/img/2015/10/27/22/10/14/53239740_ugoira600x600.zip',
        status=200,
    )
    httpretty.register_uri(
        httpretty.GET,
        'http://i1.pixiv.net/img-zip-ugoira/img/2015/10/27/22/10/14/53239740_ugoira600x600.zip',
        status=403,
    )

    with pytest.raises(PixivError):
        download_zip(53239740)


@httpretty.activate
def test_download_zip_success(fx_ugoira_body, fx_ugoira_zip):
    httpretty.register_uri(
        httpretty.GET,
        'http://www.pixiv.net/member_illust.php?mode=medium&illust_id=53239740',
        body=fx_ugoira_body,
    )
    httpretty.register_uri(
        httpretty.HEAD,
        'http://i1.pixiv.net/img-zip-ugoira/img/2015/10/27/22/10/14/53239740_ugoira600x600.zip',
        status=200,
    )
    httpretty.register_uri(
        httpretty.GET,
        'http://i1.pixiv.net/img-zip-ugoira/img/2015/10/27/22/10/14/53239740_ugoira600x600.zip',
        body=fx_ugoira_zip,
    )
    data, frames = download_zip(53239740)
    assert data == fx_ugoira_zip


@httpretty.activate
def test_make_gif(monkeypatch,
                  fx_tmpdir,
                  fx_ugoira_body,
                  fx_ugoira_zip,
                  fx_ugoira_frames):
    @contextlib.contextmanager
    def fake():
        yield str(fx_tmpdir)
    monkeypatch.setattr('tempfile.TemporaryDirectory', fake)

    httpretty.register_uri(
        httpretty.GET,
        'http://www.pixiv.net/member_illust.php?mode=medium&illust_id=53239740',
        body=fx_ugoira_body,
    )
    httpretty.register_uri(
        httpretty.HEAD,
        'http://i1.pixiv.net/img-zip-ugoira/img/2015/10/27/22/10/14/53239740_ugoira600x600.zip',
        status=200,
    )
    httpretty.register_uri(
        httpretty.GET,
        'http://i1.pixiv.net/img-zip-ugoira/img/2015/10/27/22/10/14/53239740_ugoira600x600.zip',
        body=fx_ugoira_zip,
    )
    data, frames = download_zip(53239740)
    file = fx_tmpdir / 'test.gif'
    make_gif(str(file), data, fx_ugoira_frames)
    with Image(filename=str(file)) as img:
        assert img.format == 'GIF'
        assert len(img.sequence) == 3
        assert img.sequence[0].delay == 100
        assert img.sequence[1].delay == 200
        assert img.sequence[2].delay == 300


@httpretty.activate
def test_save_zip(monkeypatch,
                  fx_tmpdir,
                  fx_ugoira_body,
                  fx_ugoira_zip,
                  fx_ugoira_frames):
    @contextlib.contextmanager
    def fake():
        yield str(fx_tmpdir)
    monkeypatch.setattr('tempfile.TemporaryDirectory', fake)

    httpretty.register_uri(
        httpretty.GET,
        'http://www.pixiv.net/member_illust.php?mode=medium&illust_id=53239740',
        body=fx_ugoira_body,
    )
    httpretty.register_uri(
        httpretty.HEAD,
        'http://i1.pixiv.net/img-zip-ugoira/img/2015/10/27/22/10/14/53239740_ugoira600x600.zip',
        status=200,
    )
    httpretty.register_uri(
        httpretty.GET,
        'http://i1.pixiv.net/img-zip-ugoira/img/2015/10/27/22/10/14/53239740_ugoira600x600.zip',
        body=fx_ugoira_zip,
    )
    data, frames = download_zip(53239740)
    file = fx_tmpdir / 'test.zip'

    save_zip(str(file), data)

    with zipfile.ZipFile(str(file)) as f:
        namelist = f.namelist()
        assert len(namelist) == len(fx_ugoira_frames)

        for filename in fx_ugoira_frames.keys():
            assert filename in namelist
