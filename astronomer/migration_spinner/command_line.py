import argparse
import importlib
import logging
import os
import time

from airflow import settings, version
from alembic.config import Config
from alembic.runtime.migration import MigrationContext
from alembic.script import ScriptDirectory


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
            source_heads = set(script_.get_heads())
            db_heads = set(context.get_current_heads())
            if source_heads == db_heads:
                logging.info('Airflow version: {}'.format(version.version))
                logging.info('Current heads: {}'.format(db_heads))
                break
            elif ticker >= timeout:
                raise TimeoutError("There are still unapplied migrations after {} "
                                   "seconds".format(ticker, timeout))
            ticker += 1
            time.sleep(1)
            logging.info('Waiting for migrations... {} second(s)'.format(ticker))


def main():
    parser = argparse.ArgumentParser(description='Airflow migration spinner.')
    parser.add_argument('--timeout', dest='timeout', default=60, type=int,
                        help='Timeout for waiting until airflow migrations completes')
    args = parser.parse_args()
    spinner(args.timeout)


if __name__ == "__main__":
    main()
