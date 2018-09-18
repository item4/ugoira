import json

from click.testing import CliRunner
import responses
from ugoira.cli import ugoira



def test_download_gif(fx_tmpdir,
                      fx_ugoira_body,
                      fx_ugoira_zip):
    """Test for command download as gif"""

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

        runner = CliRunner()
        file = fx_tmpdir / 'test.gif'
        result = runner.invoke(
            ugoira,
            ['53239740', str(file)]
        )
        assert result.exit_code == 0
        assert result.output.strip() == \
            'download completed at {} as gif'.format(str(file))

    test()


def test_is_not_ugoira(fx_non_ugoira_body):
    """Test for command download as gif"""

    @responses.activate
    def test():
        responses.reset()
        responses.add(**{
            'method': responses.GET,
            'url': 'http://www.pixiv.net/member_illust.php'
                   '?mode=medium&illust_id=53239740',
            'body': fx_non_ugoira_body,
            'content_type': 'text/html; charset=utf-8',
            'status': 200,
            'match_querystring': True,
        })

        runner = CliRunner()
        result = runner.invoke(
            ugoira,
            ['53239740', 'test.gif']
        )
        assert result.exit_code == 1
        assert result.output.strip() == \
            'Given illust-id is not ugoira.'

    test()


def test_download_zip(fx_tmpdir,
                      fx_ugoira_body,
                      fx_ugoira_zip):
    """Test for command download as zip"""

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

        runner = CliRunner()
        file = fx_tmpdir / 'test.zip'
        result = runner.invoke(
            ugoira,
            ['53239740', str(file)]
        )
        assert result.exit_code == 0
        assert result.output.strip() == \
            'download completed at {} as zip'.format(str(file))

    test()


def test_download_without_suffix(fx_tmpdir,
                                 fx_ugoira_body,
                                 fx_ugoira_zip):
    """Test for command download without suffix"""

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

        runner = CliRunner()
        file = fx_tmpdir / 'test'
        result = runner.invoke(
            ugoira,
            ['53239740', str(file)]
        )
        assert result.exit_code == 0
        assert result.output.strip() == \
            'download completed at {}.gif as gif'.format(str(file))

    test()
