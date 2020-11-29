#!/usr/bin/env python3

from pathlib import Path
from argparse import ArgumentParser
import json

from ipa.report import IPA

# MAIN

def main():
    CLI = ArgumentParser(description='Analysis of the size of an IPA file')
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
    
    args = CLI.parse_args()
    ipa_path = Path(args.ipa_path)
    external_frameworks_input_file_list = Path(args.external_frameworks_input_file_list)

    ipa_report = IPA(ipa_path=ipa_path, external_input_file_list=external_frameworks_input_file_list)

    print(json.dumps(ipa_report.as_json, indent=4))


if __name__ == '__main__':
    main()