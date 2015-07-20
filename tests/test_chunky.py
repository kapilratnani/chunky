#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

import pytest

import chunky


def test_chunky_open():
    reader = chunky.open("/tmp/test_{0}.txt", 'r')
    assert isinstance(reader, chunky.ChunkReader)
    reader.close()

    writer = chunky.open("/tmp/test_{0}.txt", 'w')
    assert isinstance(writer, chunky.ChunkWriter)
    writer.close()

    # test unsupported mode
    with pytest.raises(ValueError):
        chunky.open("/tmp/test_{0}.txt", 'a')


def file_get_contents(path):
    fp = open(path)
    contents = fp.read()
    fp.close()
    return contents


def test_chunkwriter_onefile():
    writer = chunky.open("/tmp/test_{0}.txt", 'w', 10)
    assert isinstance(writer, chunky.ChunkWriter)

    for i in range(0, 10):
        writer.write(str(i) + os.linesep)

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

    result_content = file_get_contents("/tmp/test_0.txt")
    assert expected_content.strip() == result_content.strip()


def test_chunkwriter_multiple_files():
    writer = chunky.open("/tmp/test_{0}.txt", 'w', 10)
    assert isinstance(writer, chunky.ChunkWriter)

    for i in range(0, 16):
        writer.write(str(i) + os.linesep)

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

    result_content = file_get_contents("/tmp/test_0.txt")
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

    result_content = file_get_contents("/tmp/test_1.txt")
    assert expected_content.strip() == result_content.strip()


def test_chunkwriter_exception_on_closed_file():
    writer = chunky.open("/tmp/test_{0}.txt", 'w')
    writer.close()
    with pytest.raises(ValueError):
        writer.write("test" + os.linesep)


callback_called = False

callback_count = 0


def test_chunkwriter_callback():
    def callback(filename, num_lines_written):
        global callback_called, callback_count
        callback_called = True
        callback_count += 1
        assert os.path.exists(filename)
        assert num_lines_written > 0
        assert len(file_get_contents(filename)) > 0

    writer = chunky.open(
        "/tmp/test_{0}.txt", 'w', chunk_size=10,
        cb_chunk_written=callback)

    for i in range(0, 35):
        writer.write(str(i) + os.linesep)

    writer.close()

    assert callback_called
    assert os.path.exists("/tmp/test_0.txt")
    assert os.path.exists("/tmp/test_1.txt")
    assert os.path.exists("/tmp/test_2.txt")
    assert os.path.exists("/tmp/test_3.txt")
    assert callback_count == 4


def test_chunkwriter_callback_error():
    writer = chunky.open("/tmp/test_{0}.txt", 'w', cb_chunk_written="NotACallback")

    for i in range(0, 5):
        writer.write(str(i) + os.linesep)

    with pytest.raises(ValueError):
        writer.close()


def test_chunkwriter_pattern():
    wrong_pattern = "/tmp/{0}/test.txt"
    with pytest.raises(ValueError):
        chunky.open(wrong_pattern, mode='w')

    wrong_pattern = "/tmp/test.txt"
    with pytest.raises(ValueError):
        chunky.open(wrong_pattern, mode='w')

    wrong_pattern = "/tmp/test_{0}_{1}.txt"
    with pytest.raises(ValueError):
        chunky.open(wrong_pattern, mode='w')

chunk_start_called = False
chunk_written_called = False


def test_with_csv_dictwriter():
    import csv
    csvfile = chunky.open("/tmp/csv_test_{0}.csv", mode='w', chunk_size=6)
    writer = csv.DictWriter(csvfile, fieldnames=["id", "name"])

    def chunk_start(filename):
        global chunk_start_called
        chunk_start_called = True
        writer.writeheader()
        assert filename is not None

    def chunk_written(filename, num_lines_written):
        global chunk_written_called
        chunk_written_called = True
        assert filename is not None
        assert num_lines_written > 0

    csvfile.cb_chunk_start = chunk_start
    csvfile.cb_chunk_written = chunk_written

    writer.writeheader()
    for i in range(0, 16):
        writer.writerow({"id": i, "name": "Test"})

    csvfile.close()

    assert chunk_written_called
    assert chunk_start_called

    assert os.path.exists("/tmp/csv_test_0.csv")
    assert os.path.exists("/tmp/csv_test_1.csv")
    assert os.path.exists("/tmp/csv_test_2.csv")

    num_lines = []
    for i in range(0, 3):
        fp = open("/tmp/csv_test_0.csv")
        reader = csv.DictReader(fp)
        assert reader.fieldnames == ["id", "name"]
        count = 0
        for row in reader:
            assert row["id"]
            assert row["name"]
            count += 1
        num_lines.append(count)

    assert num_lines == [5, 5, 5]

