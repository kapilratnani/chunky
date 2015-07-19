# -*- coding:utf-8 -*-
"""
Chunky
A utility class to read and write files in chunks.

Main entry-point for chunky
"""
import os
import string
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

    def __init__(self, file_pattern, chunk_size, cb_chunk_written):
        self.pattern = file_pattern
        self.__check_pattern()
        self.chunk_size = chunk_size
        self.cnum = 0
        self.line_count = 0
        self.fileobj = None
        self.cb_chunk_written = cb_chunk_written
        self.__make_new_file()

    def __check_pattern(self):
        """Replacement field should only be in filename.
        Only supported replacement field is {0}
        """
        dirname = os.path.dirname(self.pattern)
        basefilename = os.path.basename(self.pattern)
        fmt = string.Formatter()
        # check dirname. it should not have any format params
        # returns tuple  (literal_text, field_name, format_spec, conversion
        parsed = fmt.parse(dirname)
        for p in parsed:
            # p[1] is replacement field name
            if p[1] is not None:
                raise ValueError("replacement field in dirname is not supported")

        # check filename
        parsed = fmt.parse(basefilename)
        num_replacement_field = 0
        for p in parsed:
            if p[1] is not None:
                num_replacement_field += 1
                if p[1] != '0':
                    raise ValueError("Only {0} is supported")

        if num_replacement_field == 0:
            raise ValueError("one replacement field is required")

        if num_replacement_field > 1:
            raise ValueError("Only 1 replacement field is supported")

    def __make_new_file(self):
        self.__close_current()
        self.current_file = self.pattern.format(self.cnum)
        self.fileobj = py_open(self.current_file, 'w')
        self.cnum += 1

    def __close_current(self):
        if self.fileobj:
            self.fileobj.close()
            self.__notify_subscriber()
            self.fileobj = None

    def __notify_subscriber(self):
        if self.cb_chunk_written:
            if hasattr(self.cb_chunk_written, '__call__'):
                self.cb_chunk_written(self.current_file, self.line_count)
            else:
                raise ValueError("callback is not callable.")

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
        return "<ChunkWriter %s>" % self.pattern


def open(file_pattern, mode='r', chunk_size=1000, cb_chunk_written=None):
    """
    :param file_pattern: filename with a placeholder({0}) for numbering chunks
    :param mode: 'r' for read, 'w' for write
    :param chunk_size: Only for 'w' mode. This will create files containing chunks of specified number of lines
    :param cb_chunk_written: only for 'w' mode. Callback to be called when a chunk is written and closed.
    :returns: for 'r' ChunkReader and for 'w' ChunkWriter
    """
    if mode == 'r':
        return ChunkReader(file_pattern)
    elif mode == 'w':
        return ChunkWriter(file_pattern, chunk_size, cb_chunk_written)
    else:
        raise ValueError("Not a supported mode.")
