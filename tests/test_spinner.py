from unittest import mock
from unittest.mock import MagicMock, Mock

import pytest
from migration_spinner.spinner import spinner


@mock.patch('alembic.runtime.migration.MigrationContext.get_current_revision')
@mock.patch('alembic.script.base.ScriptDirectory.get_current_head')
def test_spinner_success(get_current_head, get_current_revision):
    get_current_revision.return_value = "00000000"
    get_current_head.return_value = "00000000"
    spinner(timeout=0)


@mock.patch('alembic.runtime.migration.MigrationContext.get_current_revision')
@mock.patch('alembic.script.base.ScriptDirectory.get_current_head')
def test_spinner_one_sec_timeout(get_current_head, get_current_revision):
    get_current_revision.return_value = "00000000"
    get_current_head.return_value = "10000000"
    with pytest.raises(TimeoutError):
        spinner(timeout=1)
