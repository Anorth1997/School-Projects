import unittest
import tweets


class TestCommonWords(unittest.TestCase):

    def test_none_removed1(self):
        """ Test common_words with N so that no words are removed. """

        words_to_counts = {'cat': 1}
        expected_result = {'cat': 1}
        tweets.common_words(words_to_counts, 1)
        self.assertEqual(words_to_counts, expected_result, 'none removed')

    # Place your unit test definitions after this line.
    def test_none_removed2(self):
        """ Test common_words with N is greater than len(self) so that no words
        are removed."""
        
        words_to_counts = {'cat': 1}
        expected_result = {'cat': 1}
        tweets.common_words(words_to_counts, 2)
        self.assertEqual(words_to_counts, expected_result, 'none removed') 

    def test_some_removed1(self):
        """ Test common_words with N so that some words are removed. """
        
        words_to_counts = {'you': 2, 'dont': 1, 'wish': 1, 'could': 1, \
                           'vote': 1, 'have': 2}
        expected_result = {'you': 2, 'have': 2}
        tweets.common_words(words_to_counts, 3)
        self.assertEqual(words_to_counts, expected_result)
    
    def test_all_removed2(self):
        """ Test common_words with N so that some words are removed. """
        
        words_to_counts = {'you': 2, 'dont': 1, 'wish': 1, 'could': 1, \
                           'vote': 1, 'have': 3}
        expected_result = {}
        tweets.common_words(words_to_counts, 0)
        self.assertEqual(words_to_counts, expected_result)
        
# Place your unit test definitions before this line.
if __name__ == '__main__':
    unittest.main(exit=False)
