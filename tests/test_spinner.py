from unittest import mock
from unittest.mock import MagicMock, Mock

import pytest
from migration_spinner.spinner import spinner


@mock.patch('alembic.runtime.migration.MigrationContext')
@mock.patch('alembic.script.ScriptDirectory')
def test_spinner_success(script, migration_context):
    script.from_config = Mock()
    script.from_config.get_current_head = Mock()
    script.from_config.get_current_head.return_value = "00000000"
    migration_context.configure = Mock()
    migration_context.get_current_revision = Mock()
    migration_context.get_current_revision.return_value = "00000000"
    spinner(timeout=0)


@mock.patch('alembic.runtime.migration.MigrationContext')
@mock.patch('alembic.script.ScriptDirectory')
def test_spinner_one_sec_timeout(script, migration_context):
    script.from_config = Mock()
    script.get_current_head = Mock()
    script.get_current_head.return_value = "00000000"
    migration_context.configure = Mock()
    migration_context.get_current_revision = Mock()
    migration_context.get_current_revision.return_value = "e3e4r4tf"
    with pytest.raises(TimeoutError):
        spinner(timeout=1)
