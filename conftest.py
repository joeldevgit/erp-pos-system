import pytest


def pytest_addoption(parser):
    parser.addoption("--e2e", action="store_true", default=False, help="ejecutar pruebas E2E Playwright")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--e2e"):
        return
    skip_e2e = pytest.mark.skip(reason="usa --e2e para ejecutar pruebas E2E")
    for item in items:
        if "e2e" in item.keywords:
            item.add_marker(skip_e2e)
