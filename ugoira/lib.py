import json
import pathlib
import re
import tempfile
import zipfile

from requests import Session
from wand.image import Image


user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:34.0)' + \
             ' Gecko/20100101 Firefox/34.0'

pixiv_url = {
    'index': 'http://www.pixiv.net/',
    'login': 'https://www.secure.pixiv.net/login.php',
    'image-main': ('http://www.pixiv.net/member_illust.php'
                   '?mode=medium&illust_id={}'),
}

pixiv = Session()
pixiv.headers['User-Agent'] = user_agent

ugoira_data_regex = re.compile(
    r'pixiv\.context\.ugokuIllustData\s*=\s*'
    '(\{"src":".+?","mime_type":".+?","frames":\[.+?\]\})'
)


def login(id, password):
    if id is None or password is None or not id or not password:
        raise PixivError('ID and Password must be needed.')
    if len(password) < 6:
        raise PixivError('Password is too short! Must be longer than 6.')
    if len(password) > 32:
        raise PixivError('Password is too long! Must be shorter than 32.')

    pixiv.get(pixiv_url['index'])
    rv = pixiv.post(pixiv_url['login'], data={
        'mode': 'login',
        'pixiv_id': id,
        'pass': password,
        'skip': '1'
    })
    if 'ログインの制限を開始しました' in rv.text:
        raise PixivError('Your login is restricted. Try it after.')
    return 'login.php' not in rv.url


class PixivError(Exception):
    pass


def is_ugoira(image_id: int):
    res = pixiv.get(pixiv_url['image-main'].format(image_id))
    return '_ugoku-illust-player-container' in res.text


def download_zip(image_id: int):
    image_main_url = pixiv_url['image-main'].format(image_id)
    res = pixiv.get(image_main_url)
    data = json.loads(ugoira_data_regex.search(res.text).group(1))
    pixiv.headers['Referer'] = image_main_url
    res = pixiv.head(data['src'])
    if res.status_code != 200:
        raise PixivError('Wrong image src. Please report it with image-id')
    res = pixiv.get(data['src'])
    if res.status_code != 200:
        raise PixivError('Can not download image zip')
    frames = {f['file']: f['delay'] for f in data['frames']}
    return res.content, frames


def make_gif(filename: str, file_data: bytes, frames: dict, div_by=1):
    with tempfile.TemporaryDirectory() as tmpdirname:
        file = pathlib.Path(tmpdirname) / 'temp.zip'
        with file.open('wb') as f:
            f.write(file_data)
        with zipfile.ZipFile(str(file)) as zipf:
            files = zipf.namelist()
            first_image = zipf.read(files[0])

            with Image(blob=first_image) as img:
                width = img.width
                height = img.height

            with Image(width=width,
                       height=height) as container:
                with container.convert('gif') as gif:
                    gif.sequence.clear()  # remove first empty frame
                    for file in files:
                        with Image(blob=zipf.read(file)) as part_image:
                            with part_image.convert('gif') as part_gif:
                                part = part_gif.sequence[0]
                                gif.sequence.append(part)
                                with gif.sequence[-1]:
                                    gif.sequence[-1].delay = \
                                        frames[file]//10//div_by

                    gif.save(filename=filename)


def save_zip(filename: str, blob: bytes):
    with open(filename, 'wb') as f:
        f.write(blob)
