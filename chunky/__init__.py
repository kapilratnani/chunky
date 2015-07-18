# -*- coding:utf-8 -*-
"""
Chunky
A utility class to read and write files in chunks.

Main entry-point for chunky
"""

from __builtin__ import open as py_open

__all__ = ["ChunkReader", "ChunkWriter", "open"]


class ChunkReader:
    def __init__(self, file_pattern):
        pass

    def readline(self, limit=-1):
        pass

    def close(self):
        pass

    def __repr__(self):
        return "<ChunkReader %s>" % self.file_pattern


class ChunkWriter:
    """ChunkWriter writes files in sizes of chunk_size each.
    Creates files as per the pattern specified.
    """

    def __init__(self, file_pattern, chunk_size):
        self.pattern = file_pattern
        self.chunk_size = chunk_size
        self.cnum = 0
        self.line_count = 0
        self.fileobj = None
        self.__make_new_file()

    def __make_new_file(self):
        self.__close_current()
        self.current_file = self.pattern.format(self.cnum)
        self.fileobj = py_open(self.current_file, 'w')
        self.cnum += 1

    def __close_current(self):
        if self.fileobj:
            self.fileobj.close()
            self.fileobj = None

    def writeline(self, s):
        self.__check_closed()
        if self.line_count == self.chunk_size:
            self.__make_new_file()
            self.line_count = 0
        self.fileobj.write(s + "\n")
        self.line_count += 1

    def __check_closed(self):
        if self.fileobj is None:
            raise ValueError("I/O on closed file.")

    def close(self):
        self.__close_current()

    def __repr__(self):
        return "<ChunkWriter %s>" % self.file_pattern


def open(file_pattern, mode='r', chunk_size=1000):
    """
    :param file_pattern: filename with a placeholder({0}) for numbering chunks
    :param mode: 'r' for read, 'w' for write
    :param chunk_size: Only for 'w' mode. This will create files containing chunks of specified number of lines
    :returns: for 'r' ChunkReader and for 'w' ChunkWriter
    """
    if mode == 'r':
        return ChunkReader(file_pattern)
    elif mode == 'w':
        return ChunkWriter(file_pattern, chunk_size)
    else:
        raise ValueError("No supported mode.")
