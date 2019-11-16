import os
import time

from airflow import settings, version

from alembic import script as script_
from alembic.config import Config
from alembic.runtime import migration
import logging


# package_dir is path of installed airflow in your virtualenv or system (site-packages)
# we use it to find alembic.ini file
def spinner(package_dir, timeout):
    directory = os.path.join(package_dir, 'migrations')
    config = Config(os.path.join(package_dir, 'alembic.ini'))
    config.set_main_option('script_location', directory)
    config.set_main_option('sqlalchemy.url', settings.SQL_ALCHEMY_CONN)

    script = script_.ScriptDirectory.from_config(config)
    connectable = settings.engine

    with connectable.connect() as connection:
        context = migration.MigrationContext.configure(connection)
        ticker = 0
        while True:
            if script.get_current_head() == context.get_current_revision():
                logging.info('Airflow version: {}'.format(version.version))
                logging.info('Current head: {}'.format(script.get_current_head()))
                logging.info('Current rev: {}'.format(context.get_current_revision()))
                break
            elif ticker > timeout:
                raise TimeoutError("ticker {} > timeout {}".format(ticker, timeout))
            ticker += 1
            time.sleep(1)


def main(args):
    logging.info(args)
    spinner(args.airflow_package_dir, args.timeout)
