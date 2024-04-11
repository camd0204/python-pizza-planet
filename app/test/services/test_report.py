import pytest
from ..fixtures.report import *


def test_get_report_service(client, report_uri):
    print(client)
    print(report_uri)
    response = client.get(report_uri)
    pytest.assume(response.status.startswith('200'))