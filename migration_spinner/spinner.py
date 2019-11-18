import importlib
import logging
import os
import time

from airflow import settings, version
from alembic.script import ScriptDirectory
from alembic.config import Config
from alembic.runtime.migration import MigrationContext


# package_dir is path of installed airflow in your virtualenv or system (site-packages)
# we use it to find alembic.ini file
def spinner(timeout):
    package_dir = os.path.dirname(importlib.util.find_spec('airflow').origin)
    directory = os.path.join(package_dir, 'migrations')
    config = Config(os.path.join(package_dir, 'alembic.ini'))
    config.set_main_option('script_location', directory)
    config.set_main_option('sqlalchemy.url', settings.SQL_ALCHEMY_CONN)
    script_ = ScriptDirectory.from_config(config)

    with settings.engine.connect() as connection:
        context = MigrationContext.configure(connection)
        ticker = 0
        while True:
            if script_.get_current_head() == context.get_current_revision():
                logging.info('Airflow version: {}'.format(version.version))
                logging.info('Current head: {}'.format(script_.get_current_head()))
                logging.info('Current rev: {}'.format(context.get_current_revision()))
                break
            elif ticker > timeout:
                raise TimeoutError("ticker {} > timeout {}".format(ticker, timeout))
            ticker += 1
            time.sleep(1)


def main(args):
    logging.info(args)
    spinner(args.airflow_package_dir)
