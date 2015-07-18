#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

import pytest

import chunky


def test_chunky_open():
    reader = chunky.open("/tmp/test_{0}.txt", 'r')
    assert isinstance(reader, chunky.ChunkReader)

    writer = chunky.open("/tmp/test_{0}.txt", 'w')
    assert isinstance(writer, chunky.ChunkWriter)


def fileGetContents(path):
    fp = open(path)
    contents = fp.read()
    fp.close()
    return contents


def test_chunkwriter_onefile():
    writer = chunky.open("/tmp/test_{0}.txt", 'w', 10)
    assert isinstance(writer, chunky.ChunkWriter)

    for i in range(0, 10):
        writer.writeline(str(i))

    writer.close()

    assert os.path.exists("/tmp/test_0.txt")
    expected_content = """
0
1
2
3
4
5
6
7
8
9
    """

    result_content = fileGetContents("/tmp/test_0.txt")
    assert expected_content.strip() == result_content.strip()


def test_chunkwriter_multiple_files():
    writer = chunky.open("/tmp/test_{0}.txt", 'w', 10)
    assert isinstance(writer, chunky.ChunkWriter)

    for i in range(0, 16):
        writer.writeline(str(i))

    writer.close()

    assert os.path.exists("/tmp/test_0.txt")
    expected_content = """
0
1
2
3
4
5
6
7
8
9
    """

    result_content = fileGetContents("/tmp/test_0.txt")
    assert expected_content.strip() == result_content.strip()

    assert os.path.exists("/tmp/test_1.txt")
    expected_content = """
10
11
12
13
14
15
    """

    result_content = fileGetContents("/tmp/test_1.txt")
    assert expected_content.strip() == result_content.strip()


def test_chunkwriter_exception_on_closed_file():
    writer = chunky.open("/tmp/test_{0}.txt", 'w')
    writer.close()
    with pytest.raises(ValueError):
        writer.writeline("test")