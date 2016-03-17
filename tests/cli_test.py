from click.testing import CliRunner
import responses
from ugoira.cli import ugoira


def test_too_short_password(fx_too_short_id_pw):
    """Test for command with too short password.

    It must will be fail.
    """

    id, pw = fx_too_short_id_pw
    runner = CliRunner()
    result = runner.invoke(
        ugoira,
        ['--id', id, '--password', pw, '53239740', 'test.gif']
    )
    assert result.exit_code == 1
    assert result.output.strip() == \
        'Password is too short! Must be longer than 6.'


def test_too_long_password(fx_too_long_id_pw):
    """Test for command with too long password.

    It must will be fail.
    """

    id, pw = fx_too_long_id_pw
    runner = CliRunner()
    result = runner.invoke(
        ugoira,
        ['--id', id, '--password', pw, '53239740', 'test.gif']
    )
    assert result.exit_code == 1
    assert result.output.strip() == \
        'Password is too long! Must be shorter than 32.'


def test_invalid_password(fx_invalid_id_pw):
    """Test for command with invalid id/pw pair.

    It must will be fail.

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
            'url': 'https://www.pixiv.net/login.php',
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
        # Responses is so fool. It try old mapping. So We needs some trick :(
        responses.add(**{
            'method': responses.POST,
            'url': 'http://www.pixiv.net/',
            'body': '????',
            'content_type': 'text/html; charset=utf-8',
            'status': 301,
            'adding_headers': {
                'Location': 'http://example.com/'
            },
        })

        id, pw = fx_invalid_id_pw
        runner = CliRunner()
        result = runner.invoke(
            ugoira,
            ['--id', id, '--password', pw, '53239740', 'test.gif']
        )
        assert result.exit_code == 1
        assert result.output.strip() == 'Login failed.'

    test()


def test_too_many_login_tried(fx_valid_id_pw):
    """Test for command with invalid id/pw pair.

    It must will be fail.

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
            'url': 'https://www.pixiv.net/login.php',
            'body': '誤入力が続いたため、アカウントのロックを行いました。'
                    'しばらく経ってからログインをお試しください。',
            'content_type': 'text/html; charset=utf-8',
            'status': 200,
        })

        id, pw = fx_valid_id_pw
        runner = CliRunner()
        result = runner.invoke(
            ugoira,
            ['--id', id, '--password', pw, '53239740', 'test.gif']
        )
        assert result.exit_code == 1
        assert result.output.strip() == \
            'Your login is restricted. Try it after.'

    test()


def test_download_gif(fx_tmpdir,
                      fx_valid_id_pw,
                      fx_ugoira_body,
                      fx_ugoira_zip):
    """Test for command download as gif"""

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
            'url': 'https://www.pixiv.net/login.php',
            'body': 'Just touch, Do not access it really.'
                    ' Because they block us.',
            'content_type': 'text/html; charset=utf-8',
            'status': 301,
            'adding_headers': {
                'Location': 'http://www.pixiv.net/'
            },
        })
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

        id, pw = fx_valid_id_pw
        runner = CliRunner()
        file = fx_tmpdir / 'test.gif'
        result = runner.invoke(
            ugoira,
            ['--id', id, '--password', pw, '53239740', str(file)]
        )
        assert result.exit_code == 0
        assert result.output.strip() == \
            'download completed at {} as gif'.format(str(file))

    test()


def test_is_not_ugoira(fx_valid_id_pw, fx_non_ugoira_body):
    """Test for command download as gif"""

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
            'url': 'https://www.pixiv.net/login.php',
            'body': 'Just touch, Do not access it really.'
                    ' Because they block us.',
            'content_type': 'text/html; charset=utf-8',
            'status': 301,
            'adding_headers': {
                'Location': 'http://www.pixiv.net/'
            },
        })
        responses.add(**{
            'method': responses.GET,
            'url': 'http://www.pixiv.net/member_illust.php'
                   '?mode=medium&illust_id=53239740',
            'body': fx_non_ugoira_body,
            'content_type': 'text/html; charset=utf-8',
            'status': 200,
            'match_querystring': True,
        })

        id, pw = fx_valid_id_pw
        runner = CliRunner()
        result = runner.invoke(
            ugoira,
            ['--id', id, '--password', pw, '53239740', 'test.gif']
        )
        assert result.exit_code == 1
        assert result.output.strip() == \
            'Given illust-id is not ugoira.'

    test()


def test_download_zip(fx_tmpdir,
                      fx_valid_id_pw,
                      fx_ugoira_body,
                      fx_ugoira_zip):
    """Test for command download as zip"""

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
            'url': 'https://www.pixiv.net/login.php',
            'body': 'Just touch, Do not access it really.'
                    ' Because they block us.',
            'content_type': 'text/html; charset=utf-8',
            'status': 301,
            'adding_headers': {
                'Location': 'http://www.pixiv.net/'
            },
        })
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

        id, pw = fx_valid_id_pw
        runner = CliRunner()
        file = fx_tmpdir / 'test.zip'
        result = runner.invoke(
            ugoira,
            ['--id', id, '--password', pw, '53239740', str(file)]
        )
        assert result.exit_code == 0
        assert result.output.strip() == \
            'download completed at {} as zip'.format(str(file))

    test()


def test_download_without_suffix(fx_tmpdir,
                                 fx_valid_id_pw,
                                 fx_ugoira_body,
                                 fx_ugoira_zip):
    """Test for command download without suffix"""

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
            'url': 'https://www.pixiv.net/login.php',
            'body': 'Just touch, Do not access it really.'
                    ' Because they block us.',
            'content_type': 'text/html; charset=utf-8',
            'status': 301,
            'adding_headers': {
                'Location': 'http://www.pixiv.net/'
            },
        })
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

        id, pw = fx_valid_id_pw
        runner = CliRunner()
        file = fx_tmpdir / 'test'
        result = runner.invoke(
            ugoira,
            ['--id', id, '--password', pw, '53239740', str(file)]
        )
        assert result.exit_code == 0
        assert result.output.strip() == \
            'download completed at {}.gif as gif'.format(str(file))

    test()
