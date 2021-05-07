import pytest


@pytest.fixture
def cmdopt(request):
    return request.config.getoption("--cmdopt")