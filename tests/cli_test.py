from ugoira.cli import ugoira


def test_too_short_password(fx_clirunner, fx_too_short_id_pw):
    id, pw = fx_too_short_id_pw
    result = fx_clirunner.invoke(
        ugoira,
        ['--id', id, '--password', pw, '53239740', 'test.gif']
    )
    assert result.exit_code == 1
    assert result.output.strip() == \
        'Password is too short! Must be longer than 6.'


def test_too_long_password(fx_clirunner, fx_too_long_id_pw):
    id, pw = fx_too_long_id_pw
    result = fx_clirunner.invoke(
        ugoira,
        ['--id', id, '--password', pw, '53239740', 'test.gif']
    )
    assert result.exit_code == 1
    assert result.output.strip() == \
        'Password is too long! Must be shorter than 32.'


def test_invalid_password(fx_httpretty, fx_clirunner, fx_invalid_id_pw):
    fx_httpretty.register_uri(
        fx_httpretty.GET,
        'http://www.pixiv.net/',
        body='Just touch, Do not access it really. Because they block us.',
    )
    fx_httpretty.register_uri(
        fx_httpretty.POST,
        'https://www.secure.pixiv.net/login.php',
        status=301,
        location='https://example.com/',
    )
    fx_httpretty.register_uri(
        fx_httpretty.GET,
        'https://example.com/',
        body='fail',
    )

    id, pw = fx_invalid_id_pw
    result = fx_clirunner.invoke(
        ugoira,
        ['--id', id, '--password', pw, '53239740', 'test.gif']
    )
    assert result.exit_code == 1
    assert result.output.strip() == 'Login failed.'


def test_too_many_login_tried(fx_httpretty, fx_clirunner, fx_invalid_id_pw):
    fx_httpretty.register_uri(
        fx_httpretty.GET,
        'http://www.pixiv.net/',
        body='Just touch, Do not access it really. Because they block us.',
    )
    fx_httpretty.register_uri(
        fx_httpretty.POST,
        'https://www.secure.pixiv.net/login.php',
        body='誤入力が続いたため、アカウントのロックを行いました。'
             'しばらく経ってからログインをお試しください。',
    )

    id, pw = fx_invalid_id_pw
    result = fx_clirunner.invoke(
        ugoira,
        ['--id', id, '--password', pw, '53239740', 'test.gif']
    )
    assert result.exit_code == 1
    assert result.output.strip() == 'Your login is restricted. Try it after.'
