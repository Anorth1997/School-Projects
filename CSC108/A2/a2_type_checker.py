import builtins

# Check for use of functions print and input.

# IMPORTANT!
# If you are getting this error message here:
# line 11, in <module>
#     our_print = print
# invalid syntax: <string>, line 11, pos 21
# Then you are using the wrong version of Python! Make sure you have Python 3!
our_print = print
our_input = input


def disable_print(*args):
    raise Exception("You must not call print anywhere in your code!")


def disable_input(*args):
    raise Exception("You must not call input anywhere in your code!")

builtins.print = disable_print
builtins.input = disable_input

import palindromes

# palindromes.is_palindrome
result = palindromes.is_palindrome('aba')
assert isinstance(result, bool), \
    '''palindromes.is_palindrome should return a bool, but returned {0}
       '''.format(type(result))

# palindromes.is_palindromic_phrase
result = palindromes.is_palindromic_phrase('ab.a')
assert isinstance(result, bool), \
    '''palindromes.is_palindromic_phrase should return a bool, but returned {0}
       '''.format(type(result))

# palindromes.get_odd_palindrome_at
result = palindromes.get_odd_palindrome_at('aba', 1)
assert isinstance(result, str), \
    '''palindromes.get_odd_palindrome_at should return a str, but returned {0}
       '''.format(type(result))

import dna

# dna.is_base_pair
result = dna.is_base_pair('A', 'T')
assert isinstance(result, bool), \
    '''dna.is_base_pair should return a bool, but returned {0}
       '''.format(type(result))

# dna.is_dna
result = dna.is_dna('GGATC', 'CCTAG')
assert isinstance(result, bool), \
    '''dna.is_dna should return a bool, but returned {0}
       '''.format(type(result))

# dna.is_dna_palindrome
result = dna.is_dna_palindrome('GGCC', 'CCGG')
assert isinstance(result, bool), \
    '''dna.is_dna_palindrome should return a bool, but returned {0}
       '''.format(type(result))

# dna.restriction_sites
result = dna.restriction_sites('GGCCGG', 'GG')
assert isinstance(result, list), \
    '''dna.restriction_sites should return a list, but returned {0}
       '''.format(type(result))
assert False not in [isinstance(item, int) for item in result], \
    '''dna.restriction_sites should return a list of ints, but a non-int was found
       '''

# dna.match_enzymes
result = dna.match_enzymes('GGATCC', ['BamHI'], ['GGATCC'])
assert isinstance(result, list), \
    '''dna.match_enzymes should return a list, but returned {0}
       '''.format(type(result))
assert False not in [isinstance(item, list) and len(item) == 2 and \
                     isinstance(item[0], str) and isinstance(item[1], list) and \
                     False not in [isinstance(ele, int) for ele in item[1]] for item in result], \
    '''dna.match_enzymes should return a list of (str, list of int) two-item lists, but an invalid element was found
       '''

# dna.one_cutters
result = dna.one_cutters('GGATCC', ['BamHI'], ['GGATCC'])
assert isinstance(result, list), \
    '''dna.one_cutters should return a list, but returned {0}
       '''.format(type(result))
assert False not in [isinstance(item, list) and len(item) == 2 and \
                     isinstance(item[0], str) and isinstance(item[1], int) for item in result], \
    '''dna.one_cutters should return a list of (str, int) two-item lists, but an invalid element was found
       '''

# dna.correct_mutations
strands = ['ACGTGGCCTAGCT', 'CAGTGATCG', 'ACATGGGCCGT']
result = dna.correct_mutations(strands, 'ACGGCCTT', ['HaeIII'], ['GGCC'])
assert isinstance(result, type(None)), \
    '''dna.correct_mutations should return NoneType, but returned {0}
       '''.format(type(result))

our_print("""
Hooray! The type checker passed!
This does NOT necessarily mean that your functions are correct!

It does mean that the functions in palindromes.py and dna.py:
- are named correctly,
- take the correct number of arguments, and
- return the correct types.

Be sure to thoroughly test your functions yourself before submitting.""")

builtins.print = our_print
builtins.input = our_input
