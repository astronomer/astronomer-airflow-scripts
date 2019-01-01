import argparse

import spinner


def main():
    parser = argparse.ArgumentParser(description='Airflow migration spinner.')
    parser.add_argument('--timeout', dest='timeout', default=60,
                        help='Timeout for waiting until airflow migrations completes')
    args = parser.parse_args()
    spinner.main(args)
