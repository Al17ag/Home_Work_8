import unittest   # для написания и запуска тестов
from text_processor import TextProcessor
import os


class TestTextProcessor(unittest.TestCase):

    def setUp(self):
        self.text = "Hello, World!"
        self.processor = TextProcessor(self.text)
        self.empty_text = ""
        self.numeric_text = "123 ABC!!!"
        self.stop_words = ['this', 'is']
        self.sample_text = "this is a test"

    def tearDown(self):
        pass

    def test_clean_text_removes_non_letters_and_converts_to_lowercase(self):
        self.processor.clean_text()
        self.assertEqual(self.processor.cleaned_text, 'hello world')

    def test_clean_text_with_numeric_text(self):
        self.processor.text = self.numeric_text
        self.processor.clean_text()
        self.assertEqual(self.processor.cleaned_text,'abc')

    def test_clean_text_with_empty_string(self):
        self.processor.text = self.empty_text
        self.processor.clean_text()
        self.assertEqual(self.processor.cleaned_text, '')

    def test_remove_stop_words(self):
        self.processor.text = self.sample_text
        self.processor.clean_text()
        self.processor.remove_stop_words(self.stop_words)
        self.assertEqual(self.processor.cleaned_text, 'a test')

    def test_remove_stop_words_without_prior_cleaning(self):
        self.processor.text = self.sample_text
        self.processor.remove_stop_words(self.stop_words)
        self.assertEqual(self.processor.cleaned_text, 'a test')

    def test_remove_stop_words_with_empty_stop_words(self):
        self.processor.text = "hello world"
        self.processor.remove_stop_words([])
        self.assertEqual(self.processor.cleaned_text, 'hello world')


if __name__ == '__main__':
    unittest.main()
