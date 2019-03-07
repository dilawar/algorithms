# About

Compress and decompress a file using Huffman codes. Huffman codes are
prefix-free code.

# Requirements

Python version 3.5 or higher. Package `huffman` module from PyPi. 

    python3 -m pip install huffman 

# Compress

To compress a file (e.g. `war_and_peace.txt`), run the following command.

    python3 war_and_peace.txt -c 

It will generate a compressed file `war_and_peace.txt.dx`. 

# Decompress

To decompress `war_and_peace.txt.dx` file. Run the following command.

    python3 war_and_peace.txt.dx -d 

It will print the uncompressed file to `stdout` (terminal). You can make sure
they are the same.

# Performance

This implementation is slow (since it is in pure python). And achieves a
compression ratio of 1.5 to 1.8. On `WAR AND PEACE` from project Gutenberg
[https://www.gutenberg.org/files/2600/2600-0.txt], we achieve a compression
ratio of 1.77.
