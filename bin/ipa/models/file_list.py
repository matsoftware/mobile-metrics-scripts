#!/usr/bin/env python3

import re
from typing import List, Optional
from pathlib import Path

class FileList(object):
    @staticmethod
    def read_input_file_lists(internal_input_file_list: Path) -> List[str]:
        with open(internal_input_file_list, 'r') as input_list:
            return [v for v in [FileList.parse_input(f) for f in input_list.readlines()] if v]

    @staticmethod
    def parse_input(value: str) -> Optional[str]:
        r_format = r"(\w*).framework$"
        result = value.strip()
        if (result.startswith('#')):
            return None
        if (not result.endswith('.framework')):
            return None
        pattern = re.compile(r_format)
        match_pattern = pattern.search(result)
        if match_pattern:
            return match_pattern.group(1)
        else:
            return None