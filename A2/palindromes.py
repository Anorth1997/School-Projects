
def is_palindrome(possible_palindrome):
    """(str) -> bool
    Precondiction: the possible_palindrome consists of only lowercase 
    alphabetic letters.
    
    Return True iff the possible_palindrome is a palindrome.
    >>> is_palindrome('aabbcc')
    False
    >>> is_palindrome('nursesrun')
    True
    """
    return possible_palindrome == possible_palindrome[::-1]

def is_palindromic_phrase(possible_palindrome):
    """(str) -> bool
    
    Return True iff the possible_palindrome is a palindrome which ignores case
    and non-alphabetic characters.
    
    >>> is_palindromic_phrase('Madam, Im Adam.') 
    True
    >>> is_palindromic_phrase('a1b2c9c3b3a0') 
    True
    """
    result = ''
    
    for i in range(len(possible_palindrome)):
        if possible_palindrome[i].isalpha():
            if possible_palindrome[i].isupper():
                result = result + possible_palindrome[i].lower()
            else:
                result = result + possible_palindrome[i]
    result_bool = is_palindrome(result)
    return result_bool

def get_odd_palindrome_at(possible_palin,i):
    """(str, int) -> str
    Precondition: len(possible_palin) >= i >= 0, and possible_palin
    is consisting of only lowercase letters.
    
    Return the longest odd-length palindrome in the possible_palind that 
    is centered at the specificed index i.
    
    >>> get_odd_palindrome_at('dededed', 3)
    'dededed'
    >>> get_odd_palindrome_at('nmabcbaio' , 4)
    'abcba'
    """
    result = possible_palin[i]
    h = range(len(possible_palin))
    u = 1
    while (i + u in h) and (i - u in h):
        if possible_palin[i - u] == possible_palin[i + u]:
            result = possible_palin[i-u] + result + possible_palin[i+u]
        u = u + 1
    return result

if __name__ == '__main__':
    import doctest
    doctest.testmod()