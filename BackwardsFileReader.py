# --------- License Info ---------
# Copyright 2015 Emind Systems Ltd. - htttp://www.emind.co

import os

"""
Reads a file backwards, line by line, while also maintaining the position of the cursor (which is
the beginning of the last line read).

Usage example:
    bfr = BackwardsFileReader(file)
    for line in bfr.read_lines():
        print "(" + str(bfr.current_line_pos) + "): " + line
"""
class BackwardsFileReader:
    def __init__(self, file):
        self.file = file

    def read_lines(self, buffer_size=65536):
        # Calculate the size of the file.
        self.file.seek(0, os.SEEK_END)
        size = self.file.tell()

        # Set the initial cursor position; imagine there's a '\n' after the file and point after it.
        self.current_line_pos = size + 1

        # Calculate the initial position to read from.
        n_buffers = (size - 1) // buffer_size + 1
        chunk_pos = (n_buffers - 1) * buffer_size

        # We need to keep saving the first line of the current chunk and append it to the next
        # chunk, as it's very likely that it is NOT a complete line.
        leftover = ''

        while chunk_pos >= 0:
            # Read a new chunk from the file.
            self.file.seek(chunk_pos, os.SEEK_SET)
            buffer = self.file.read(buffer_size)

            # Split the buffer in lines (considering Unix line endings).
            lines = buffer.split('\n')

            # Do something with the leftover, if any.
            if leftover:
                # If the previous chunk started right from the beginning of a line, yield the
                # leftover as a separate line.
                if buffer[-1] is '\n':
                    self.current_line_pos = chunk_pos + buffer_size
                    yield leftover
                # Otherwise, concatenate the leftover to the last line of this chunk.
                else:
                    lines[-1] += leftover

            # Yield all non-empty lines in this chunk, except the first one (saved as leftover).
            for index in range(len(lines) - 1, 0, -1):
                if lines[index]:
                    self.current_line_pos -= (1 + len(lines[index]))
                    yield lines[index]
                else:
                    self.current_line_pos -= 1
            leftover = lines[0]

            # Calculate the next position to read from.
            chunk_pos -= buffer_size

        # Yield the leftover, if any. This should be the first line of the file.
        self.current_line_pos = 0
        if leftover:
            yield leftover
