import pathlib
import zipfile

from pytest import fixture

from wand.color import Color
from wand.image import Image


@fixture
def fx_tmpdir(tmpdir):
    """Make :class:`pathlib.Path` instance of ```tmpdir```."""

    return pathlib.Path(str(tmpdir))


@fixture
def fx_ugoira_body():
    """Ugoira page data."""

    return '{"error":false,"message":"","body":{"src":"https:\/\/i.pximg.net\/img-zip-ugoira\/img\/2019\/04\/29\/16\/09\/38\/74442143_ugoira600x600.zip","originalSrc":"https:\/\/i.pximg.net\/img-zip-ugoira\/img\/2019\/04\/29\/16\/09\/38\/74442143_ugoira1920x1080.zip","mime_type":"image\/jpeg","frames":[{"file":"000000.jpg","delay":70},{"file":"000001.jpg","delay":70},{"file":"000002.jpg","delay":70},{"file":"000003.jpg","delay":70},{"file":"000004.jpg","delay":70},{"file":"000005.jpg","delay":70},{"file":"000006.jpg","delay":70},{"file":"000007.jpg","delay":70},{"file":"000008.jpg","delay":70},{"file":"000009.jpg","delay":70},{"file":"000010.jpg","delay":70},{"file":"000011.jpg","delay":70},{"file":"000012.jpg","delay":70},{"file":"000013.jpg","delay":70},{"file":"000014.jpg","delay":70},{"file":"000015.jpg","delay":70},{"file":"000016.jpg","delay":70},{"file":"000017.jpg","delay":70},{"file":"000018.jpg","delay":70},{"file":"000019.jpg","delay":70},{"file":"000020.jpg","delay":70},{"file":"000021.jpg","delay":70},{"file":"000022.jpg","delay":70},{"file":"000023.jpg","delay":70},{"file":"000024.jpg","delay":70},{"file":"000025.jpg","delay":70},{"file":"000026.jpg","delay":70},{"file":"000027.jpg","delay":70},{"file":"000028.jpg","delay":70},{"file":"000029.jpg","delay":70},{"file":"000030.jpg","delay":70},{"file":"000031.jpg","delay":70},{"file":"000032.jpg","delay":70},{"file":"000033.jpg","delay":70},{"file":"000034.jpg","delay":70},{"file":"000035.jpg","delay":70},{"file":"000036.jpg","delay":70},{"file":"000037.jpg","delay":70},{"file":"000038.jpg","delay":70},{"file":"000039.jpg","delay":70},{"file":"000040.jpg","delay":70},{"file":"000041.jpg","delay":70},{"file":"000042.jpg","delay":70},{"file":"000043.jpg","delay":70},{"file":"000044.jpg","delay":70},{"file":"000045.jpg","delay":70},{"file":"000046.jpg","delay":70},{"file":"000047.jpg","delay":70},{"file":"000048.jpg","delay":70},{"file":"000049.jpg","delay":70},{"file":"000050.jpg","delay":70},{"file":"000051.jpg","delay":70},{"file":"000052.jpg","delay":70},{"file":"000053.jpg","delay":70},{"file":"000054.jpg","delay":70},{"file":"000055.jpg","delay":70},{"file":"000056.jpg","delay":70},{"file":"000057.jpg","delay":70},{"file":"000058.jpg","delay":70},{"file":"000059.jpg","delay":70},{"file":"000060.jpg","delay":70},{"file":"000061.jpg","delay":70},{"file":"000062.jpg","delay":70},{"file":"000063.jpg","delay":70},{"file":"000064.jpg","delay":70},{"file":"000065.jpg","delay":70},{"file":"000066.jpg","delay":70},{"file":"000067.jpg","delay":70},{"file":"000068.jpg","delay":70},{"file":"000069.jpg","delay":70},{"file":"000070.jpg","delay":70},{"file":"000071.jpg","delay":70},{"file":"000072.jpg","delay":70},{"file":"000073.jpg","delay":70},{"file":"000074.jpg","delay":70},{"file":"000075.jpg","delay":70},{"file":"000076.jpg","delay":70}]}}'  # noqa


@fixture
def fx_non_ugoira_body():
    """Non ugoira page data."""

    return '{"error":true,"message":"\uc9c0\uc815\ud55c ID\ub294 \uc6b0\uace0\uc774\ub77c\uac00 \uc544\ub2d9\ub2c8\ub2e4","body":[]}'  # noqa

@fixture
def fx_ugoira_zip(fx_tmpdir):
    """
    Generates a zip file used in testing
    instead of downloading an actual ugoira.
    """

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
