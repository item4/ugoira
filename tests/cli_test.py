from click.testing import CliRunner

import responses

from ugoira.cli import ugoira
from ugoira.lib import get_metadata_url

ugoira_id = 74442143
non_ugoira_id = 74073488
zip_url = 'https://i.pximg.net/img-zip-ugoira/img/2019/' \
          '04/29/16/09/38/74442143_ugoira600x600.zip'
big_zip_url = 'https://i.pximg.net/img-zip-ugoira/img/' \
              '2019/04/29/16/09/38/74442143_ugoira1920x1080.zip'


def test_download(fx_tmpdir, fx_ugoira_body, fx_ugoira_zip, fx_ugoira_big_zip):
    """Test for command download"""

    @responses.activate
    def case1():
        """
        original head - good
        original get - good
        common head - not reached
        common get - not reached
        """
        responses.reset()
        responses.add(**{
            'method': responses.GET,
            'url': get_metadata_url(ugoira_id),
            'body': fx_ugoira_body,
            'content_type': 'application/json',
            'status': 200,
            'match_querystring': True,
        })
        responses.add(**{
            'method': responses.HEAD,
            'url': big_zip_url,
            'status': 200,
        })
        responses.add(**{
            'method': responses.GET,
            'url': big_zip_url,
            'body': fx_ugoira_big_zip,
            'content_type': 'application/zip',
            'status': 200,
        })

        runner = CliRunner()
        result = runner.invoke(
            ugoira,
            [str(ugoira_id)]
        )
        assert result.exit_code == 0
        assert result.output.strip() == (
            'Downloading {} (0/1)\n'.format(ugoira_id) +
            'Download was completed successfully.'
            ' format is {} and output path is {}{}'.format(
                'gif',
                ugoira_id,
                '.gif',
            )
        )

    @responses.activate
    def case2():
        """
        original head - good
        original get - bad
        common head - good
        common get - good
        """
        responses.reset()
        responses.add(**{
            'method': responses.GET,
            'url': get_metadata_url(ugoira_id),
            'body': fx_ugoira_body,
            'content_type': 'application/json',
            'status': 200,
            'match_querystring': True,
        })
        responses.add(**{
            'method': responses.HEAD,
            'url': big_zip_url,
            'status': 200,
        })
        responses.add(**{
            'method': responses.GET,
            'url': big_zip_url,
            'status': 403,
        })
        responses.add(**{
            'method': responses.HEAD,
            'url': zip_url,
            'status': 200,
        })
        responses.add(**{
            'method': responses.GET,
            'url': zip_url,
            'body': fx_ugoira_zip,
            'content_type': 'application/zip',
            'status': 200,
        })

        runner = CliRunner()
        result = runner.invoke(
            ugoira,
            [str(ugoira_id)]
        )
        assert result.exit_code == 0
        assert result.output.strip() == (
            'Downloading {} (0/1)\n'.format(ugoira_id) +
            'Download was completed successfully.'
            ' format is {} and output path is {}{}'.format(
                'gif',
                ugoira_id,
                '.gif',
            )
        )

    @responses.activate
    def case3():
        """
        original head - bad
        original get - not reached
        common head - good
        common get - good
        """
        responses.reset()
        responses.add(**{
            'method': responses.GET,
            'url': get_metadata_url(ugoira_id),
            'body': fx_ugoira_body,
            'content_type': 'application/json',
            'status': 200,
            'match_querystring': True,
        })
        responses.add(**{
            'method': responses.HEAD,
            'url': big_zip_url,
            'status': 403,
        })
        responses.add(**{
            'method': responses.HEAD,
            'url': zip_url,
            'status': 200,
        })
        responses.add(**{
            'method': responses.GET,
            'url': zip_url,
            'body': fx_ugoira_zip,
            'content_type': 'application/zip',
            'status': 200,
        })

        runner = CliRunner()
        result = runner.invoke(
            ugoira,
            [str(ugoira_id)]
        )
        assert result.exit_code == 0
        assert result.output.strip() == (
            'Downloading {} (0/1)\n'.format(ugoira_id) +
            'Download was completed successfully.'
            ' format is {} and output path is {}{}'.format(
                'gif',
                ugoira_id,
                '.gif',
            )
        )

    case1()
    case2()
    case3()


def test_error(fx_tmpdir, fx_ugoira_body, fx_ugoira_zip):
    """Test for encount PixivError"""

    @responses.activate
    def case1():
        """
        original head - bad
        original get - not reached
        common head - bad
        common get - not reached
        """
        responses.reset()
        responses.add(**{
            'method': responses.GET,
            'url': get_metadata_url(ugoira_id),
            'body': fx_ugoira_body,
            'content_type': 'application/json',
            'status': 200,
            'match_querystring': True,
        })
        responses.add(**{
            'method': responses.HEAD,
            'url': big_zip_url,
            'status': 503,
        })
        responses.add(**{
            'method': responses.HEAD,
            'url': zip_url,
            'status': 503,
        })

        runner = CliRunner()
        result = runner.invoke(
            ugoira,
            [str(ugoira_id)]
        )
        assert result.output.strip().startswith(
            'Downloading {} (0/1)\nError: '.format(ugoira_id)
        )

    @responses.activate
    def case2():
        """
        original head - good
        original get - bad
        common head - bad
        common get - not reached
        """
        responses.reset()
        responses.add(**{
            'method': responses.GET,
            'url': get_metadata_url(ugoira_id),
            'body': fx_ugoira_body,
            'content_type': 'application/json',
            'status': 200,
            'match_querystring': True,
        })
        responses.add(**{
            'method': responses.HEAD,
            'url': big_zip_url,
            'status': 200,
        })
        responses.add(**{
            'method': responses.GET,
            'url': big_zip_url,
            'status': 403,
        })
        responses.add(**{
            'method': responses.HEAD,
            'url': zip_url,
            'status': 503,
        })

        runner = CliRunner()
        result = runner.invoke(
            ugoira,
            [str(ugoira_id)]
        )
        assert result.output.strip().startswith(
            'Downloading {} (0/1)\nError: '.format(ugoira_id)
        )

    @responses.activate
    def case3():
        """
        original head - bad
        original get - not reached
        common head - good
        common get - bad
        """
        responses.reset()
        responses.add(**{
            'method': responses.GET,
            'url': get_metadata_url(ugoira_id),
            'body': fx_ugoira_body,
            'content_type': 'application/json',
            'status': 200,
            'match_querystring': True,
        })
        responses.add(**{
            'method': responses.HEAD,
            'url': big_zip_url,
            'status': 503,
        })
        responses.add(**{
            'method': responses.HEAD,
            'url': zip_url,
            'status': 200,
        })
        responses.add(**{
            'method': responses.GET,
            'url': zip_url,
            'status': 403,
        })

        runner = CliRunner()
        result = runner.invoke(
            ugoira,
            [str(ugoira_id)]
        )
        assert result.output.strip().startswith(
            'Downloading {} (0/1)\nError: '.format(ugoira_id)
        )

    case1()
    case2()
    case3()


def test_is_not_ugoira(fx_non_ugoira_body):
    """Test for command download as gif"""

    @responses.activate
    def test():
        responses.reset()
        responses.add(**{
            'method': responses.GET,
            'url': get_metadata_url(non_ugoira_id),
            'body': fx_non_ugoira_body,
            'content_type': 'application/json',
            'status': 200,
            'match_querystring': True,
        })

        runner = CliRunner()
        result = runner.invoke(
            ugoira,
            [str(non_ugoira_id)]
        )
        assert result.output.strip() == (
            'Downloading {} (0/1)\n'.format(non_ugoira_id) +
            'Error: Illust ID {} is not ugoira.'.format(non_ugoira_id)
        )

    test()
