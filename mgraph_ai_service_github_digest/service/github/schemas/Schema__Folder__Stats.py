from typing                                                                       import List
from osbot_utils.type_safe.Type_Safe                                              import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt                              import Safe_UInt
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path import Safe_Str__File__Path


class Schema__Folder__Stats(Type_Safe):
    path             : Safe_Str__File__Path                                         # Folder path
    depth            : Safe_UInt                                                    # Depth level (0 = root)
    size_bytes       : Safe_UInt                                                    # Total size of all files in folder (recursive)
    file_count       : Safe_UInt                                                    # Number of files (recursive)
    direct_file_count: Safe_UInt                                                    # Number of files directly in this folder
    subfolder_count  : Safe_UInt                                                    # Number of immediate subfolders
    extensions       : List[str]                                                    # Unique extensions in folder