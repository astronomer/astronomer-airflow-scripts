from unittest import mock

import pytest

from astronomer.migration_spinner.command_line import spinner


@mock.patch('alembic.runtime.migration.MigrationContext.get_current_heads')
@mock.patch('alembic.script.base.ScriptDirectory.get_heads')
def test_spinner_success(get_heads, get_current_heads):
    get_heads.return_value = ["00000000"]
    get_current_heads.return_value = ["00000000"]
    spinner(timeout=0)


@mock.patch('alembic.runtime.migration.MigrationContext.get_current_heads')
@mock.patch('alembic.script.base.ScriptDirectory.get_heads')
def test_spinner_one_sec_timeout(get_heads, get_current_heads):
    get_current_heads.return_value = ["00000000"]
    get_heads.return_value = ["10000000"]
    with pytest.raises(TimeoutError):
        spinner(timeout=1)
