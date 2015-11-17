import httpretty
import pytest
from ugoira.lib import PixivError, download_zip, is_ugoira, login


def test_login_valid(fx_valid_id_pw):
    assert login(*fx_valid_id_pw)


def test_login_pw_is_too_short(fx_too_short_id_pw):
    with pytest.raises(PixivError):
        login(*fx_too_short_id_pw)


def test_login_invalid(fx_invalid_id_pw):
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
