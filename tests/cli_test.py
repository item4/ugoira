from click.testing import CliRunner
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

    import httpretty

    @httpretty.activate
    def test():
        httpretty.register_uri(
            httpretty.GET,
            'http://www.pixiv.net/',
            body='Just touch, Do not access it really. Because they block us.',
        )
        httpretty.register_uri(
            httpretty.POST,
            'https://www.secure.pixiv.net/login.php',
            status=301,
            location='https://example.com/',
        )
        httpretty.register_uri(
            httpretty.GET,
            'https://example.com/',
            body='fail',
        )

        id, pw = fx_invalid_id_pw
        runner = CliRunner()
        result = runner.invoke(
            ugoira,
            ['--id', id, '--password', pw, '53239740', 'test.gif']
        )
        assert result.exit_code == 1
        assert result.output.strip() == 'Login failed.'

    try:
        test()
    finally:
        httpretty.disable()
        httpretty.reset()
        del httpretty


def test_too_many_login_tried(fx_invalid_id_pw):
    """Test for command with invalid id/pw pair.

    It must will be fail.

    Known issue: This test was broken with another tests. Must run it solo.
    """

    import httpretty

    @httpretty.activate
    def test():
        httpretty.register_uri(
            httpretty.GET,
            'http://www.pixiv.net/',
            body='Just touch, Do not access it really. Because they block us.',
        )
        httpretty.register_uri(
            httpretty.POST,
            'https://www.secure.pixiv.net/login.php',
            body='誤入力が続いたため、アカウントのロックを行いました。'
                 'しばらく経ってからログインをお試しください。',
        )

        id, pw = fx_invalid_id_pw
        runner = CliRunner()
        result = runner.invoke(
            ugoira,
            ['--id', id, '--password', pw, '53239740', 'test.gif']
        )
        assert result.exit_code == 1
        assert result.output.strip() == \
            'Your login is restricted. Try it after.'

    try:
        test()
    finally:
        httpretty.disable()
        httpretty.reset()
        del httpretty
