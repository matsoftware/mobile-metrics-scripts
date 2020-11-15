#!/usr/bin/env python3

from pathlib import Path
from argparse import ArgumentParser
import logging

from ipa.report import IPA

# MAIN

def main():
    CLI = ArgumentParser(description='Analysis of the ')
    CLI.add_argument(
        '--ipa-path',
        metavar='A',
        type=str,
        required=True,
        help='The path to the IPA file'
    )
    CLI.add_argument(
        '--external-frameworks-input-file-list',
        metavar='E',
        type=str,
        required=True,
        help='The path to xcfilelist file containing the list of names of libraries considered external to the project.'
    )
    CLI.add_argument(
        '--metrics-host',
        metavar='E',
        type=str,
        required=False,
        help='The host for the mobile metrics API.'
    )
    
    args = CLI.parse_args()
    ipa_path = Path(args.ipa_path)
    external_frameworks_input_file_list = Path(args.external_frameworks_input_file_list)
    metrics_host = args.metrics_host

    logging.basicConfig(level=logging.DEBUG)

    logging.debug('Start IPA size analysis ...')

    ipa_report = IPA(ipa_path=ipa_path, external_input_file_list=external_frameworks_input_file_list)

    if metrics_host:
        # TO IMPLEMENT
        logging.debug(f'Storing metrics report for {ipa_report.name}')

    ditto = ipa_report.__dict__

    logging.debug('IPA size analysis terminated.')

if __name__ == '__main__':
    main()