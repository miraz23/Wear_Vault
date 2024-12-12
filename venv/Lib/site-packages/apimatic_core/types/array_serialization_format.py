from enum import Enum


class SerializationFormats(Enum):
    """Enumeration of Array serialization formats

    Attributes:
        UN_INDEXED: Unindexed array serialization format
        INDEXED: Indexed array serialization format
        PLAIN: Plain array serialization format
        CSV: Comma separated array serialization format
        TSV: Tab separated array serialization format
        PSV: Pipe separated array serialization format

    """

    UN_INDEXED = "unindexed"
    INDEXED = "indexed"
    PLAIN = "plain"
    CSV = "csv"
    TSV = "tsv"
    PSV = "psv"
