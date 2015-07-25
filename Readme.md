# Chunky  [![Build Status](https://travis-ci.org/kapilratnani/chunky.svg?branch=master)](https://travis-ci.org/kapilratnani/chunky)
--------------
A python module to handle reading and writing of text files in chunks. Automatically creates files when the specified chunk size is reached. It provides a familiar interface of io.TextIOBase for easy integration with existing python IO facilities.



## Installation
--------------
```
pip install chunky
```


## Usage
-----------------

### Writing files
Chunky creates files based on the specified pattern. The placeholder '{0}' starts with '0' for the first file and is incremented each time the number of lines reaches the specified chunk size.

Below example creates 3 files with names:

- a_file_0.txt - 10 lines
- a_file_1.txt - 10 lines
- a_file_2.txt - 5 lines

```python
import chunky

fileobj = chunky.open("a_file_{0}.txt", "w", chunk_size = 10)
for i in range(0, 25):
    fileobj.write("%d\n" % i)

fileobj.close()
```

### Reading files
Reading is quite straightforward. Based on the specified pattern each file is read starting from chunk 0.
```python
import chunky

with chunky.open("a_file_{0}.txt","r") as f:
    for line in f:
        print line
```

## Callbacks
---------------
Chunky accepts callback functions to notify start and close of a chunk.

- cb_chunk_closed(filename, num_lines_written)
- cb_chunk_start(filename)
```python
import chunky

def closed_callback(filename, num_lines_written):
    print "wrote %d lines in file:%s" % (num_lines_written, filename)

def start_callback(filename):
    print "writing to file:%s" % filename

writer = chunky.open(
    "test_{0}.txt", 'w', chunk_size=10,
    cb_chunk_closed=closed_callback,
    cb_chunk_start=start_callback)

for i in range(0, 35):
    writer.write("%d\n" % i)

writer.close()
```