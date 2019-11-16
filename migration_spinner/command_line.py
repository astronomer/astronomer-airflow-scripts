import os
import site

import spinner
import argparse


def check_airflow_package(value):
    if not os.path.exists(value):
        raise argparse.ArgumentTypeError("Airflow was not found in path: %s" % value)
    return value


def main():
    default_airflow_package_dir = os.path.join(site.getsitepackages()[0], 'airflow')
    if not os.path.exists(default_airflow_package_dir):
        raise FileNotFoundError('Airflow was not found in default site-packages path: %s'
                                % default_airflow_package_dir)

    parser = argparse.ArgumentParser(description='Airflow migration spinner.')
    parser.add_argument('--timeout', dest='timeout', default=60,
                        help='Timeout for waiting until airflow migrations completes')
    parser.add_argument('--airflow_package_dir', dest='airflow_package_dir',
                        default=default_airflow_package_dir, type=check_airflow_package,
                        help='Timeout for waiting until airflow migrations completes')
    args = parser.parse_args()
    spinner.main(args)
