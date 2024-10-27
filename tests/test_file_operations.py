import unittest
from file_operations import write_to_file, read_from_file
import os

class TestFileOperation(unittest.TestCase):
    def setUp(self):
        self.file_name = 'test.json'
        self.test_data = {
            "pk": 4,
            "title": "Test Title",
            "author": "Test Author",
            "published_date": "2024-06-23",
            "publisher": 6,
            "price": 9.99,
            "discounted_price": 3.56,
            "is_bestseller": True,
            "is_banned": False,
            "genres": [1, 2, 3]
        }

    def tearDown(self):  # выполняется после каждого теста
        if os.path.exists(self.file_name):
            os.remove(self.file_name)  # Если файл существует, он удаляется с помощью функции os.remove

    def test_write_and_read_file(self):
        write_to_file(self.file_name, self.test_data)
        data = read_from_file(self.file_name)
        self.assertEqual(data, self.test_data)

    def test_write_and_read_empty_file(self):
            write_to_file(self.file_name, {})
            data = read_from_file(self.file_name)
            self.assertEqual(data, {})

    def test_read_nonexistent_file(self):
            with self.assertRaises(FileNotFoundError):
                read_from_file('nonexistent_file.json')

    def test_write_bad_data_into_file(self):
            with self.assertRaises(TypeError):
                write_to_file(self.file_name, set(['invalid', 'data']))

if __name__ == '__main__':
        unittest.main()













