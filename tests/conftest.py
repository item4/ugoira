import os
import pathlib
import zipfile

from click.testing import CliRunner
from pytest import fixture, skip, yield_fixture
from wand.color import Color
from wand.image import Image


def pytest_addoption(parser):
    parser.addoption('--pixiv-id', default=os.getenv('PIXIV_ID', None))
    parser.addoption('--pixiv-password',
                     default=os.getenv('PIXIV_PASSWORD', None))


@fixture
def fx_tmpdir(tmpdir):
    """Make :class:`pathlib.Path` instance of ```tmpdir```."""

    return pathlib.Path(str(tmpdir))


@fixture
def fx_valid_id_pw(request):
    """Pixiv ID/PW pair tester given."""

    try:
        id = request.config.getoption('--pixiv-id')
    except ValueError:
        skip('This test must need --pixiv-id.')
    if id is None:
        skip('This test must need --pixiv-id.')

    try:
        password = request.config.getoption('--pixiv-password')
    except ValueError:
        skip('This test must need --pixiv-password.')
    if password is None:
        skip('This test must need --pixiv-password.')

    return id, password


@fixture
def fx_too_short_id_pw():
    """Too short password case."""

    return 'test', '1'


@fixture
def fx_too_long_id_pw():
    """Too long password case."""

    return 'test', '1'*33


@fixture
def fx_invalid_id_pw():
    """Invalid ID/PW pair case."""
    return 'invalid_id', 'invalid_pw'


@fixture
def fx_clirunner():
    """:mod:`click` CLI test Runner"""
    return CliRunner()


@fixture
def fx_ugoira_body():
    """Ugoira page data."""

    with open('./tests/mock/ugoira.html') as f:
        return f.read().encode('u8')


@fixture
def fx_non_ugoira_body():
    """Non ugoira page data."""

    with open('./tests/mock/non_ugoira.html') as f:
        return f.read().encode('u8')


@fixture
def fx_ugoira_zip(fx_tmpdir):
    """Make ugoira zip file for test."""

    file = fx_tmpdir / '00000000_ugoira600x600.zip'
    imgs = [
        fx_tmpdir / '000000.jpg',
        fx_tmpdir / '000001.jpg',
        fx_tmpdir / '000002.jpg',
    ]
    colors = [
        Color('red'),
        Color('blue'),
        Color('green'),
    ]
    for path, color in zip(imgs, colors):
        with Image(width=100, height=100, background=color) as img:
            img.save(filename=str(path))

    with zipfile.ZipFile(str(file), 'w') as f:
        for img in imgs:
            f.write(str(img), img.name)

    with file.open('rb') as f:
        return f.read()


@fixture
def fx_ugoira_frames():
    """frames data."""

    return {
        '000000.jpg': 1000,
        '000001.jpg': 2000,
        '000002.jpg': 3000,
    }
