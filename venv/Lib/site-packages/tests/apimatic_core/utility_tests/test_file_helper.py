from apimatic_core.utilities.file_helper import FileHelper
from tests.apimatic_core.base import Base


class TestFileHelper(Base):

    def test_get_file(self):
        file_url = 'https://gist.githubusercontent.com/asadali214/' \
                   '0a64efec5353d351818475f928c50767/raw/8ad3533799ecb4e01a753aaf04d248e6702d4947/testFile.txt'
        actualFile = FileHelper.get_file(file_url)
        assert actualFile is not None \
               and actualFile.read() == 'This test file is created to test CoreFileWrapper ' \
                                        'functionality'.encode('ascii')
