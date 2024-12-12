import tempfile

import requests


class FileHelper:
    """A Helper Class for files.

        Attributes:
            cache (Set): Class variable which stores hashes of file URLs so we don't
                download the same file twice in a test session.

        """

    cache = {}

    @classmethod
    def get_file(cls, url):
        """Class method which takes a URL, downloads the file (if not
        already downloaded for this test session) and returns a file object for
        the file in read-binary mode.

        Args:
            url (string): The URL of the required file.
        Returns:
            FileObject: The file object of the required file (opened with "rb").

        """
        if url not in cls.cache:
            cls.cache[url] = tempfile.NamedTemporaryFile()
            cls.cache[url].write(requests.get(url).content)
        cls.cache[url].seek(0)
        return cls.cache[url]
