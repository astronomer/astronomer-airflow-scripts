import logging
import sys


def spinner():
    import os

    from airflow import settings, version

    from alembic import script
    from alembic.config import Config
    from alembic.runtime import migration

    package_dir = "/Users/andrii/work/airflow/airflow"
    directory = os.path.join(package_dir, 'migrations')

    config = Config(os.path.join(package_dir, 'alembic.ini'))
    config.set_main_option('script_location', directory)
    config.set_main_option('sqlalchemy.url', settings.SQL_ALCHEMY_CONN)

    script = script.ScriptDirectory.from_config(config)
    connectable = settings.engine

    with connectable.connect() as connection:
        context = migration.MigrationContext.configure(connection)
        print('Airflow version: {}'.format(version.version))
        print('Current head: {}'.format(script.get_current_head()))
        print('Current rev: {}'.format(context.get_current_revision()))


def main(argv):
    logging.basicConfig(level=logging.DEBUG)
    print(argv)


if __name__ == '__main__':
    main(sys.argv[1:])
