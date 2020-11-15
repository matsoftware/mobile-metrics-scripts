#!/usr/bin/env python3

from dataclasses import dataclass
from typing import List,Dict,Optional
from pathlib import Path
import re
import subprocess
from functools import reduce

from .models.size import Size, toMB
from .models.collection import Collection
from .models.compressed_files import CompressedFile
from .models.file_list import FileList

# Patterns to analyze
framework_name_pattern = r"([a-zA-Z]*?).framework"
assets_car_pattern = r"Payload/.*.app/(Assets.car)$"
executable_pattern = r"Payload/(.*).app/\1$"
file_extensions_to_analyze = [
    # Ext - Description
    ("png", "Raw images"),
    ("car", "Compressed assets"),
    ("jpg", "Raw images"),
    ("pdf", "Raw assets"),
    ("nib", "Deprecated interfaces"),
    ("storyboardc", "Deprecated interfaces"),
    ("css", "Web content"),
    ("html", "Web content"),
    ("js", "Web content")
]

def file_extension_pattern(extension: str) -> str:
    return f'(?i)[a-zA-Z]*?.({extension})$'


# IPA Analysis
    
class IPA(object):
    def __init__(self, ipa_path: Path, external_input_file_list: Path):
        self.size = 0
        self.uncompressed_size = 0
        self.name = ipa_path.name
        self.assets_car = {}
        self.executable = {}
        self.files_ext = {}
        self.__analyze(ipa_path, self.__read_compressed_files__(ipa_path), FileList.read_input_file_lists(external_input_file_list))

    # Properties
    # Stored: size, name

    @property
    def external_frameworks_size(self) -> 'Size':
        return self.__collections_size(self.external_frameworks)

    @property
    def internal_frameworks_size(self) -> 'Size':
        return self.__collections_size(self.internal_frameworks)

    @property
    def executable_name(self) -> str:
        return list(self.executable.keys())[0]

    @property
    def executable_size(self) -> 'Size':
        return self.executable[self.executable_name].size

    @property
    def asset_car_size(self) -> 'Size':
        return self.assets_car['Assets.car'].size


    def file_ext_size(self, ext: str) -> 'Size':
        if ext in self.files_ext:
            return self.files_ext[ext].size
        base_size = self.executable_size
        # Empty size
        return Size(
            compressed_size_in_mb=0,
            total_archive_compressed_size_in_mb=base_size.total_archive_compressed_size_in_mb,
            uncompressed_size_in_mb=0,
            total_archive_uncompressed_size_in_mb=base_size.total_archive_uncompressed_size_in_mb
        )

    def complementary_file_size(self, file_types: List[str]) -> 'Size':
        size_of_known_files = reduce(lambda x, y: x+y, [self.file_ext_size(ext) for ext in file_types])
        return Size(
            compressed_size_in_mb=size_of_known_files.total_archive_compressed_size_in_mb - size_of_known_files.compressed_size_in_mb,
            total_archive_compressed_size_in_mb=size_of_known_files.total_archive_compressed_size_in_mb,
            uncompressed_size_in_mb=size_of_known_files.total_archive_uncompressed_size_in_mb - size_of_known_files.uncompressed_size_in_mb,
            total_archive_uncompressed_size_in_mb=size_of_known_files.total_archive_uncompressed_size_in_mb
        )

    # Export

    @property
    def as_json(self) -> Dict:
        internal_frameworks_table = Collection.export_collections(self.internal_frameworks)
        external_frameworks_table = Collection.export_collections(self.external_frameworks)
        file_ext_table = dict([(f"{ext[1]} (*.{ext[0]})", self.file_ext_size(ext[0]).as_dict) for ext in file_extensions_to_analyze])
        return {
                "ipa": self.name,
                "total_universal_IPA_size_in_mb": self.size,
                "total_uncompressed_app_size_in_mb": self.uncompressed_size,
                "external_frameworks": external_frameworks_table,
                "internal_frameworks": internal_frameworks_table,
                "Asset.car": self.asset_car_size.as_dict,
                "executable_name": self.executable_name,
                "main_executable_size": self.executable_size.as_dict,
                "extensions": file_ext_table
        }

    # Analysis methods

    @staticmethod
    def __read_compressed_files__(path: Path) -> List['CompressedFile']:
        zip_content = str(subprocess.check_output(["unzip", "-v",str(path)])).split("\\n")[3:-1]
        raw_compressed_files = [f.split() for f in zip_content]
        total = raw_compressed_files[-1]
        total_size = CompressedFile(
            uncompressed_file_size=toMB(int(total[0])),
            file_size=toMB(int(total[1])), 
            file_compression=float(total[2][:-1]), 
            file_name='Total'
        )
        return [CompressedFile(
            uncompressed_file_size=toMB(int(f[0])),
            file_size=toMB(int(f[2])), 
            file_compression=float(f[3][:-1]), 
            file_name=f[7]
        ) for f in raw_compressed_files[0:-2] if f[0] != "0"] + [ total_size ]

    def __analyze(self, ipa_path: Path, compressed_files: List['CompressedFile'], external_framework_names: List[str]) -> List['Framework']:
        frameworks = {}

        # Global size analysis from latest element in unzip -v result
        self.size = compressed_files[-1].file_size
        self.uncompressed_size = compressed_files[-1].uncompressed_file_size

        # To group stats around files that follow a specific pattern, please add the 
        # tuple of `dictionary` and `regex pattern` to the list below
        # To analyze a specific file extension, extend the `file_extensions_to_analyze` array
        analysis_patterns = [
            (frameworks, framework_name_pattern), # Framework
            (self.assets_car, assets_car_pattern), # Root Assets.car
            (self.executable, executable_pattern), # Main executable
        ] + [(self.files_ext, file_extension_pattern(ext[0])) for ext in file_extensions_to_analyze]

        for compressed_file in compressed_files:
            for group, regex_pattern in analysis_patterns:
                self.__classify(
                    group=group,
                    regex_pattern=regex_pattern,
                    compressed_file=compressed_file,
                    total_archive_size=self.size,
                    total_archive_uncompressed_size=self.uncompressed_size
                )
            
        self.__classify_frameworks(frameworks, external_framework_names)

    @staticmethod
    def __classify(group: Dict[str, 'Collection'], regex_pattern: str, compressed_file: 'CompressedFile', total_archive_size: float, total_archive_uncompressed_size: float):
            pattern = re.compile(regex_pattern)
            match_pattern = pattern.search(compressed_file.file_name)
            if match_pattern:
                match_name = match_pattern.group(1)
                if not group.get(match_name):
                    group[match_name] = Collection(
                        name=match_name,
                        total_archive_compressed_size=total_archive_size,
                        total_archive_uncompressed_size_in_mb=total_archive_uncompressed_size,
                        files=[]
                    ) 
                collection = group.get(match_name)
                collection.files.append(compressed_file)

    def __classify_frameworks(self, frameworks: Dict[str, 'Collection'], external_framework_names: List[str]):
        self.internal_frameworks = []
        self.external_frameworks = []
        for framework_name, collection in frameworks.items():
            if framework_name in external_framework_names:
                self.external_frameworks.append(collection)
            else:
                self.internal_frameworks.append(collection)
        IPA.__sort_collections(self.internal_frameworks)
        IPA.__sort_collections(self.external_frameworks)

    @staticmethod
    def __sort_collections(collections: List['Collection']):
        collections.sort(key= lambda i: i.size, reverse=True)

    def __collections_size(self, collections: List['Collection']) -> 'Size':
        return reduce(lambda x, y: x+y, [f.size for f in collections])
