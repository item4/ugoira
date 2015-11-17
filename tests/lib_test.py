import httpretty
import pytest
from ugoira.lib import PixivError, is_ugoira, login


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
