#!/usr/bin/env python3

from typing import Dict, List
from .size import Size
from functools import reduce
import operator


class Collection(object):
    def __init__(self, name: str, total_archive_compressed_size: float, total_archive_uncompressed_size_in_mb: float, files: list):
        self.name = name
        self.total_archive_compressed_size = total_archive_compressed_size
        self.total_archive_uncompressed_size_in_mb = total_archive_uncompressed_size_in_mb
        self.files = files
    
    def __hash__(self):
      return hash((self.name))

    @property
    def size(self) -> 'Size':
        totals = reduce(lambda x, y: tuple(map(operator.add, x, y)), [(f.file_size, f.uncompressed_file_size) for f in self.files])
        return Size(
            compressed_size_in_mb=totals[0],
            total_archive_compressed_size_in_mb=self.total_archive_compressed_size,
            uncompressed_size_in_mb=totals[1],
            total_archive_uncompressed_size_in_mb=self.total_archive_uncompressed_size_in_mb
        )

    @property
    def as_dict(self) -> Dict[str, str]:
        return {**{"name": self.name}, **self.size.as_dict}

    @staticmethod
    def export_collections(collections: List['Collection']) -> List[Dict[str, str]]:
        return [c.as_dict for c in collections]