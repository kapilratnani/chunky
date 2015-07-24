# -*- coding:utf-8 -*-
"""
Chunky
A utility to read and write files in chunks.

Inspired from gzip.py in python 2.7 standard library.
"""
import io
import os
import string
from __builtin__ import open as py_open

__author__ = ('Kapil Ratnani', 'kapil.ratnani@iiitb.net')

__all__ = ["ChunkedTextFile", "open"]


class ChunkedTextFile(io.TextIOBase):
    """ChunkedTextFile
        A class for reading and writing files which are split into
        number of files of fixed chunk size; Chunk size is number of
        lines. This gives a familiar abstraction of interacting with
        files without dealing with

        In write mode, on each call to write() it records the number of
        lines written (by counting newline characters) and when the
        number of lines reaches the specified chunk size, a new file
        is created and writing continues in the new file.

        In read mode, it starts reading from the first file till EOF
        and continues to other file, if any.

        Files are created/read based on the pattern specified.
        In write mode, increments the number placeholder each time the
        line count reaches the chunk size.
        In read mode, it reads each file which satisfies the pattern
        till EOF, and stops when no files are found having the pattern.
        The reading is in the order of creation.
    """

    def __init__(self, mode, file_pattern, chunk_size,
                 cb_chunk_closed, cb_chunk_start):
        """Constructor for the ChunkWriter class

        :param file_pattern: pattern which specifies the names of
        files to be created.
        Example: /tmp/test_20150723_{0}.txt . This will generate
        file names as
        /tmp/test_20150723_0.txt, /tmp/test_20150723_1.txt ...
        :param chunk_size: maximum number of lines in a chunk
        :param cb_chunk_closed: callback for notifying end of a chunk
        :param cb_chunk_start: callback for notifying start of a chunk
        """
        self.mode = mode
        self.pattern = file_pattern
        self.__check_pattern()
        self.chunk_size = chunk_size
        self.cnum = 0
        self.line_count = 0
        self.fileobj = None
        self.cb_chunk_closed = cb_chunk_closed
        self.cb_chunk_start = cb_chunk_start
        self.__init_new_file()

    def __check_pattern(self):
        """Replacement field should only be in filename.
        Only supported replacement field is {0}
        """
        dirname = os.path.dirname(self.pattern)
        basefilename = os.path.basename(self.pattern)
        fmt = string.Formatter()
        # check dirname. it should not have any replacement field
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

    def __make_next_filename(self):
        self.current_file = self.pattern.format(self.cnum)
        self.cnum += 1

    def __init_new_file(self):
        self.__make_next_filename()
        self.fileobj = py_open(self.current_file, self.mode)
        self.__notify_chunk_start()

    def __close_current(self):
        if self.fileobj:
            self.fileobj.close()
            self.__notify_chunk_closed()
            self.fileobj = None

    def __notify_chunk_closed(self):
        if self.cb_chunk_closed:
            if hasattr(self.cb_chunk_closed, '__call__'):
                self.cb_chunk_closed(self.current_file, self.line_count)
            else:
                raise ValueError("callback is not callable.")

    def __notify_chunk_start(self):
        if self.cb_chunk_start:
            if hasattr(self.cb_chunk_start, '__call__'):
                self.cb_chunk_start(self.current_file)
            else:
                raise ValueError("callback is not callable.")

    def write(self, s):
        self.__check_closed()
        self.__check_writable()
        if self.line_count == self.chunk_size:
            self.__close_current()
            self.line_count = 0
            self.__init_new_file()
        self.fileobj.write(s)
        self.line_count += s.count(os.linesep)

    def __check_writable(self):
        if self.mode != 'w':
            raise IOError("File not open for writing")

    def __check_readable(self):
        if self.mode != 'r':
            raise IOError("File not open for reading")

    def readline(self):
        self.__check_closed()
        self.__check_readable()
        line = self.fileobj.readline()
        if not line:
            self.__close_current()
            try:
                self.__init_new_file()
                return self.readline()
            except IOError:
                return line
        else:
            return line

    def readable(self):
        return self.mode == 'r'

    def writable(self):
        return self.mode == 'w'

    def seekable(self):
        return False

    def __check_closed(self):
        if self.fileobj is None:
            raise ValueError("I/O on closed file.")

    def close(self):
        self.__close_current()

    def __repr__(self):
        return "<ChunkedTextFile %s>" % self.pattern


def open(file_pattern, mode='r', chunk_size=1000,
         cb_chunk_closed=None, cb_chunk_start=None):
    """
    :param file_pattern: filename with a placeholder({0}) for numbering chunks
    :param mode: 'r' for read, 'w' for write
    :param chunk_size: Only for 'w' mode. This will create files containing chunks of specified number of lines
    :param cb_chunk_closed: Callback to be called when a chunk is closed.
     In write mode, when the chunk size is reached and the file is closed.
     In read mode, when the the current chunk is read till EOF.
    :param cb_chunk_start: Callback to be called when a new chunk starts
    :returns: ChunkedTextFile
    """
    if mode == 'w' or mode == 'r':
        return ChunkedTextFile(mode, file_pattern, chunk_size,
                               cb_chunk_closed, cb_chunk_start)
    else:
        raise ValueError("Not a supported mode.")
