from click.testing import CliRunner

from ugoira.cli import ugoira
from ugoira.lib import get_metadata_url


def test_download_case1(
    ugoira_id,
    meta_body,
    small_zip_url,
    big_zip_url,
    small_image_zip,
    big_image_zip,
    httpx_mock,
):
    """Test for command download

    original head - good
    original get - good
    common head - not reached
    common get - not reached
    """
    httpx_mock.add_response(
        method="GET",
        url=get_metadata_url(ugoira_id),
        json=meta_body,
        status_code=200,
    )
    httpx_mock.add_response(
        method="HEAD",
        url=big_zip_url,
        status_code=200,
    )
    httpx_mock.add_response(
        method="GET",
        url=big_zip_url,
        content=big_image_zip,
        headers={"content-type": "application/zip"},
        status_code=200,
    )

    runner = CliRunner()
    result = runner.invoke(ugoira, [str(ugoira_id)])
    assert result.exit_code == 0
    assert result.output.strip() == (
        f"Downloading {ugoira_id} (0/1)\n"
        + "Download was completed successfully."
        " format is {} and output path is {}{}".format(
            "gif",
            ugoira_id,
            ".gif",
        )
    )


def test_download_case2(
    ugoira_id,
    meta_body,
    small_zip_url,
    big_zip_url,
    small_image_zip,
    big_image_zip,
    httpx_mock,
):
    """Test for command download

    original head - good
    original get - bad
    common head - good
    common get - good
    """
    httpx_mock.add_response(
        method="GET",
        url=get_metadata_url(ugoira_id),
        json=meta_body,
        status_code=200,
    )
    httpx_mock.add_response(
        method="HEAD",
        url=big_zip_url,
        status_code=200,
    )
    httpx_mock.add_response(
        method="GET",
        url=big_zip_url,
        status_code=403,
    )
    httpx_mock.add_response(
        method="HEAD",
        url=small_zip_url,
        status_code=200,
    )
    httpx_mock.add_response(
        method="GET",
        url=small_zip_url,
        content=small_image_zip,
        headers={"content-type": "application/zip"},
        status_code=200,
    )

    runner = CliRunner()
    result = runner.invoke(ugoira, [str(ugoira_id)])
    assert result.exit_code == 0
    assert result.output.strip() == (
        f"Downloading {ugoira_id} (0/1)\n"
        + "Download was completed successfully."
        " format is {} and output path is {}{}".format(
            "gif",
            ugoira_id,
            ".gif",
        )
    )


def test_download(
    ugoira_id,
    meta_body,
    small_zip_url,
    big_zip_url,
    small_image_zip,
    big_image_zip,
    httpx_mock,
):
    """Test for command download

    original head - bad
    original get - not reached
    common head - good
    common get - good
    """
    httpx_mock.add_response(
        method="GET",
        url=get_metadata_url(ugoira_id),
        json=meta_body,
        status_code=200,
    )
    httpx_mock.add_response(
        method="HEAD",
        url=big_zip_url,
        status_code=403,
    )
    httpx_mock.add_response(
        method="HEAD",
        url=small_zip_url,
        status_code=200,
    )
    httpx_mock.add_response(
        method="GET",
        url=small_zip_url,
        content=small_image_zip,
        headers={"content-type": "application/zip"},
        status_code=200,
    )

    runner = CliRunner()
    result = runner.invoke(ugoira, [str(ugoira_id)])
    assert result.exit_code == 0
    assert result.output.strip() == (
        f"Downloading {ugoira_id} (0/1)\n"
        + "Download was completed successfully."
        " format is {} and output path is {}{}".format(
            "gif",
            ugoira_id,
            ".gif",
        )
    )


def test_error_case1(
    ugoira_id,
    meta_body,
    small_zip_url,
    big_zip_url,
    httpx_mock,
):
    """Test for encount PixivError

    original head - bad
    original get - not reached
    common head - bad
    common get - not reached
    """
    httpx_mock.add_response(
        method="GET",
        url=get_metadata_url(ugoira_id),
        json=meta_body,
        status_code=200,
    )
    httpx_mock.add_response(
        method="HEAD",
        url=big_zip_url,
        status_code=503,
    )
    httpx_mock.add_response(
        method="HEAD",
        url=small_zip_url,
        status_code=503,
    )

    runner = CliRunner()
    result = runner.invoke(ugoira, [str(ugoira_id)])
    assert result.output.strip().startswith(
        f"Downloading {ugoira_id} (0/1)\nError: ",
    )


def test_error_case2(
    ugoira_id,
    meta_body,
    small_zip_url,
    big_zip_url,
    httpx_mock,
):
    """Test for encount PixivError

    original head - good
    original get - bad
    common head - bad
    common get - not reached
    """
    httpx_mock.add_response(
        method="GET",
        url=get_metadata_url(ugoira_id),
        json=meta_body,
        status_code=200,
    )
    httpx_mock.add_response(
        method="HEAD",
        url=big_zip_url,
        status_code=200,
    )
    httpx_mock.add_response(
        method="GET",
        url=big_zip_url,
        status_code=403,
    )
    httpx_mock.add_response(
        method="HEAD",
        url=small_zip_url,
        status_code=503,
    )

    runner = CliRunner()
    result = runner.invoke(ugoira, [str(ugoira_id)])
    assert result.output.strip().startswith(
        f"Downloading {ugoira_id} (0/1)\nError: ",
    )


def test_error_case3(
    ugoira_id,
    meta_body,
    small_zip_url,
    big_zip_url,
    httpx_mock,
):
    """Test for encount PixivError

    original head - bad
    original get - not reached
    common head - good
    common get - bad
    """
    httpx_mock.add_response(
        method="GET",
        url=get_metadata_url(ugoira_id),
        json=meta_body,
        status_code=200,
    )
    httpx_mock.add_response(
        method="HEAD",
        url=big_zip_url,
        status_code=503,
    )
    httpx_mock.add_response(
        method="HEAD",
        url=small_zip_url,
        status_code=200,
    )
    httpx_mock.add_response(
        method="GET",
        url=small_zip_url,
        status_code=403,
    )

    runner = CliRunner()
    result = runner.invoke(ugoira, [str(ugoira_id)])
    assert result.output.strip().startswith(
        f"Downloading {ugoira_id} (0/1)\nError: ",
    )


def test_is_not_ugoira(
    non_ugoira_id,
    error_meta_body,
    httpx_mock,
):
    """Test for command download as gif"""

    httpx_mock.add_response(
        method="GET",
        url=get_metadata_url(non_ugoira_id),
        json=error_meta_body,
        status_code=200,
    )

    runner = CliRunner()
    result = runner.invoke(ugoira, [str(non_ugoira_id)])
    assert (
        result.output.strip() == f"Downloading {non_ugoira_id} (0/1)\n"
        f"Error: Illust ID {non_ugoira_id} is not ugoira."
    )
