#!/usr/bin/env python3

from dataclasses import dataclass

def toMB(size_in_bytes: int) -> float:
    return size_in_bytes / ( 1024 * 1024 )

def formattedSize(size_in_mb: float) -> str:
    return f'{size_in_mb:.1f}'


class Size(object):
    def __init__(self, compressed_size_in_mb: float, total_archive_compressed_size_in_mb: float, uncompressed_size_in_mb: float, total_archive_uncompressed_size_in_mb: float):
        
        self.total_archive_compressed_size_in_mb = total_archive_compressed_size_in_mb
        self.total_archive_uncompressed_size_in_mb = total_archive_uncompressed_size_in_mb
        
        self.compressed_size_in_mb = compressed_size_in_mb
        self.relative_compressed_size = (compressed_size_in_mb / total_archive_compressed_size_in_mb) * 100
        self.uncompressed_size_in_mb = uncompressed_size_in_mb
        self.relative_uncompressed_size = (uncompressed_size_in_mb / total_archive_uncompressed_size_in_mb) * 100

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
    def description(self) -> str:
        return f"""Compressed size: {formattedSize(self.compressed_size_in_mb)} MB
        Relative compressed size: {formattedSize(self.relative_compressed_size)}% \\\\
        Uncompressed size: {formattedSize(self.uncompressed_size_in_mb)} MB
        Relative uncompressed size: {formattedSize(self.relative_uncompressed_size)}%
        """