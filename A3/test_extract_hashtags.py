import unittest
import tweets


class TestExtractHashtags(unittest.TestCase):

    def test_no_hashtags(self):
        """ Test extract_hashtags with a tweet with no hashtags. """

        actual_hashtags = tweets.extract_hashtags('this is a tweet!')
        expected_hashtags = []
        self.assertEqual(actual_hashtags, expected_hashtags, 'empty list')

    # Place your unit test definitions after this line.
    def test_extract_hashtags1(self):
        """ Test extract_hashtags with a tweet with one hashtag. """
        
        actual_hashtags = tweets.extract_hashtags("__#lll, #dd,d dasfads")
        expected_hashtags = ['dd']
        self.assertEqual(actual_hashtags, expected_hashtags)
    
    def test_extract_hashtags2(self):
        """ Test extract_hashtags with a tweet with three empty hashtags. """
        
        actual_hashtags = tweets.extract_hashtags("__#lll, # # # ")
        expected_hashtags = ['']
        self.assertEqual(actual_hashtags, expected_hashtags)
    
    def test_extract_hashtags3(self):
        """ Test extract_hashtags with a tweet with three same hashtags. """
        
        actual_hashtags = tweets.extract_hashtags("__#lll, #CAT, #CAT #cat")
        expected_hashtags = ['CAT']
        self.assertEqual(actual_hashtags, expected_hashtags)

# Place your unit test definitions before this line.
if __name__ == '__main__':
    unittest.main(exit=False)
