"""
This class is made to enable relative seeking using file object.

Since python 3.x does not allow relative seeking, we will be achieving this using file seeker and read.
"""

import os
import logging


class FileStringIOError(Exception):
    """
    Exception class for FileStringIO.

    This will be raise for any exception in operation of the class
    """
    pass


class FileStringIO:
    def __init__(self, file_name):
        if os.path.isfile(file_name):
            try:
                self.file_obj = open(file_name, encoding="utf-8")
            except:
                raise FileStringIOError

    def read(self, size=None):
        """

        :param size: int
        Bytes.  read at most size bytes, returned as bytes. # Refer ro file.read() operation.

        :return:
        Content
        In non-blocking mode, returns None if no data is available.
        On end-of-file, returns ''
        """

        if size is None:
            return self.file_obj.read()
        else:
            return self.file_obj.read(size)

    def seek(self, offset, whence=0):
        """
        File Seeker. seeks in a file from offset to whence.

        :param offset: int
        Move to new file position and return the file position.

        :param whence: int
        seek upper bound.

        :return:
        """
        if whence == 0:
            self.file_obj.seek(offset)
        else:
            if whence == os.SEEK_END:
                # Read till EOF
                while True:
                    buffer = self.file_obj.read()
                    if not buffer:
                        break

            # Seek from current position + offset.
            self.file_obj.seek(self.file_obj.tell() + offset)
