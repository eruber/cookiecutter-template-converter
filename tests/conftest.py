# -*- coding: utf-8 -*-
"""
conftest
--------

Pytest fixtures
"""
import pytest

from click.testing import CliRunner


@pytest.fixture
def runner():
    return CliRunner()
