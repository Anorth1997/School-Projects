import unittest
import palindromes

class TestPalindromes(unittest.TestCase):
    """Example unittest test methods for get_odd_palindrome_at."""
    
    def test_palindromes_example_1(self):
        """Test get_odd_palindrome_at with 'dededed' and 3"""
        
        actual = palindromes.get_odd_palindrome_at('dededed', 3)
        expected = 'dededed'
        self.assertEqual(actual, expected)
    
    def test_palindromes_example_2(self):
        """Test get_odd_palindrome_at with 'nmabcbaio' and 4."""
        
        actual = palindromes.get_odd_palindrome_at('nmabcbaio' , 4)
        expected = 'abcba'
        self.assertEqual(actual, expected)
        

        
if __name__ == '__main__':
    unittest.main(exit=False)