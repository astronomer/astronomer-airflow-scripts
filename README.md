# Set of astronomer cli-tools.

## Usage `airflow-cleanup-pods`

```bash
$ airflow-cleanup-pods -h
usage: airflow-cleanup-pods [-h] [--namespace NAMESPACE]

Clean up k8s pods in evicted/failed/succeeded states.

optional arguments:
  -h, --help            show this help message and exit
  --namespace NAMESPACE
                        Namespace
```

## Usage `airflow-migration-spinner`

```
airflow-migration-spinner --timeout 5
[2019-11-18 19:25:04,083] {spinner.py:40} INFO - Namespace(timeout=5)
[2019-11-18 19:25:04,085] {migration.py:130} INFO - Context impl SQLiteImpl.
[2019-11-18 19:25:04,086] {migration.py:137} INFO - Will assume non-transactional DDL.
[2019-11-18 19:25:05,113] {spinner.py:36} INFO - Waiting for migrations... 1 second(s)
[2019-11-18 19:25:06,115] {spinner.py:36} INFO - Waiting for migrations... 2 second(s)
[2019-11-18 19:25:07,116] {spinner.py:36} INFO - Waiting for migrations... 3 second(s)
[2019-11-18 19:25:08,117] {spinner.py:36} INFO - Waiting for migrations... 4 second(s)
[2019-11-18 19:25:09,122] {spinner.py:36} INFO - Waiting for migrations... 5 second(s)
[2019-11-18 19:25:10,125] {spinner.py:36} INFO - Waiting for migrations... 6 second(s)
Traceback (most recent call last):
  File "/Users/andrii/.pyenv/versions/airflow-core/bin/airflow-migration-spinner", line 11, in <module>
    load_entry_point('airflow-migration-spinner', 'console_scripts', 'airflow-migration-spinner')()
  File "/Users/andrii/work/airflow-migration-spinner/migration_spinner/command_line.py", line 11, in main
    spinner.main(args)
  File "/Users/andrii/work/airflow-migration-spinner/migration_spinner/spinner.py", line 41, in main
    spinner(args.timeout)
  File "/Users/andrii/work/airflow-migration-spinner/migration_spinner/spinner.py", line 33, in spinner
    "seconds".format(ticker, timeout))
TimeoutError: There are still unapplied migrations after: 6 seconds
```

## Release

1. Build wheel
```bash
pip install -U wheel
python setup.py sdist bdist_wheel
ls -la dist
total 24
drwxr-xr-x   4 andrii  staff   128 Nov 19 14:55 .
drwxr-xr-x  22 andrii  staff   704 Nov 19 14:55 ..
-rw-r--r--   1 andrii  staff  2615 Nov 19 14:55 airflow-migration-spinner-0.0.1.tar.gz
-rw-r--r--   1 andrii  staff  6629 Nov 19 14:55 airflow_migration_spinner-0.0.1-py3-none-any.whl
```

2. Upload to github releases page


Copyright © 2019 Astronomer Inc. See LICENSE for further details.
