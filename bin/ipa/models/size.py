#!/usr/bin/env python3

from typing import Dict

def toMB(size_in_bytes: int) -> float:
    return size_in_bytes / ( 1024 * 1024 )

class Size(object):
    def __init__(self, compressed_size_in_mb: float, total_archive_compressed_size_in_mb: float, uncompressed_size_in_mb: float, total_archive_uncompressed_size_in_mb: float):
        
        self.total_archive_compressed_size_in_mb = total_archive_compressed_size_in_mb
        self.total_archive_uncompressed_size_in_mb = total_archive_uncompressed_size_in_mb
        
        self.compressed_size_in_mb = compressed_size_in_mb
        self.relative_compressed_size = (compressed_size_in_mb / total_archive_compressed_size_in_mb)
        self.uncompressed_size_in_mb = uncompressed_size_in_mb
        self.relative_uncompressed_size = (uncompressed_size_in_mb / total_archive_uncompressed_size_in_mb)

    def __add__(self, other):
        return Size(
            compressed_size_in_mb=self.compressed_size_in_mb + other.compressed_size_in_mb,
            total_archive_compressed_size_in_mb=self.total_archive_compressed_size_in_mb,
            uncompressed_size_in_mb=self.uncompressed_size_in_mb + other.uncompressed_size_in_mb,
            total_archive_uncompressed_size_in_mb=self.total_archive_uncompressed_size_in_mb
        )

    def __lt__(self, other):
        return self.compressed_size_in_mb < other.compressed_size_in_mb

    @property
    def as_dict(self) -> Dict[str, str]:
        return {
            "compressed_size_in_mb": self.compressed_size_in_mb,
            "relative_compressed_size": self.relative_compressed_size,
            "uncompressed_size_in_mb": self.uncompressed_size_in_mb,
            "relative_uncompressed_size": self.relative_uncompressed_size
        }