from unittest.mock import patch, MagicMock

from migration_spinner.spinner import spinner


def test_spinner_zero_timeout():
    spinner(0)


@patch('alembic.script.ScriptDirectory.from_config.get_current_head')
def test_spinner_one_sec_timeout(get_current_head):
    get_current_head = MagicMock()
    spinner(1)
