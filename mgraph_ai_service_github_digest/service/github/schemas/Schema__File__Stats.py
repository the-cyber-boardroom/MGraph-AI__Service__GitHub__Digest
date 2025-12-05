from osbot_utils.type_safe.Type_Safe                                              import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt                              import Safe_UInt
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Name import Safe_Str__File__Name
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path import Safe_Str__File__Path


class Schema__File__Stats(Type_Safe):
    path       : Safe_Str__File__Path                                               # Full file path
    name       : Safe_Str__File__Name                                               # File name only
    extension  : Safe_Str__File__Name                                               # File extension (e.g., '.py') | todo: this should be a specific 'extension' primitive
    size_bytes : Safe_UInt                                                          # Size in bytes
    folder     : Safe_Str__File__Path                                               # Parent folder path