#!/usr/bin/env python3

from dataclasses import dataclass

@dataclass
class CompressedFile(object):
    uncompressed_file_size: int
    file_size: int
    file_compression: float
    file_name: str
