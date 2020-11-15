#!/usr/bin/env python3

from dataclasses import dataclass
from typing import Dict
from .size import Size, toMB
from functools import reduce
import operator


@dataclass        
class Collection(object):
    name: str
    total_archive_compressed_size: float
    total_archive_uncompressed_size_in_mb: float
    files = []

    def __hash__(self):
      return hash((self.name))

    @property
    def size(self) -> 'Size':
        totals = reduce(lambda x, y: tuple(map(operator.add, x, y)), [(toMB(f.file_size), toMB(f.uncompressed_file_size)) for f in self.files])
        return Size(
            compressed_size_in_mb=totals[0],
            total_archive_compressed_size_in_mb=self.total_archive_compressed_size,
            uncompressed_size_in_mb=totals[1],
            total_archive_uncompressed_size_in_mb=self.total_archive_uncompressed_size_in_mb
        )

    @property
    def as_dict(self) -> Dict[str, str]:
        return {
            "Name": self.name,
            "Total compressed size (MB)": formattedSize(self.size.compressed_size_in_mb),
            "Relative compressed size": f'{formattedSize(self.size.relative_compressed_size)}%',
            "Total uncompressed size (MB)": formattedSize(self.size.uncompressed_size_in_mb),
            "Relative uncompressed size": f'{formattedSize(self.size.relative_uncompressed_size)}%'
        }