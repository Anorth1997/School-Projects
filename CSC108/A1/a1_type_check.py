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

import admission_functions

# Type check admission_functions.is_special_case
result = admission_functions.is_special_case('Jacqueline Smith,Best High School,2002,MAT,90,94,ENG,92,88,CHM,80,85,BArts')
assert isinstance(result, bool), \
    '''admission_functions.is_special_case should return a bool, but returned {0}
       '''.format(type(result))


# Type check admission_functions.get_final_mark
record = 'Paul Gries,Ithaca High School,1986,BIO,60,70,CHM,80,90,CAT,10,20,BEng'
result = admission_functions.get_final_mark(record, '10', '20')
assert isinstance(result, float), \
    '''admission_functions.get_final_mark should return a float, but returned {0}
       '''.format(type(result))


# Type check admission_functions.get_both_marks
result = admission_functions.get_both_marks('ABC,10,20', 'ABC')
assert isinstance(result, str), \
    '''admission_functions.get_both_marks should return a str, but returned {0}
       '''.format(type(result))


# Type check admission_functions.extract_course
result = admission_functions.extract_course('ABC,10,20', 1)
assert isinstance(result, str), \
    '''admission_functions.extract_course should return a str, but returned {0}
       '''.format(type(result))


# Type check admission_functions.applied_to_degree
record = 'Paul Gries,Ithaca High School,1986,BIO,60,70,CHM,80,90,CAT,95,96,BEng'
result = admission_functions.applied_to_degree(record, 'BEng')
assert isinstance(result, bool), \
    '''admission_functions.applied_to_degree should return a bool, but returned {0}
       '''.format(type(result))


# Type check admission_functions.decide_admission
valid_strings = ['accept', 'reject', 'accept with scholarship']
for x in [18, 22, 30]:
    result = admission_functions.decide_admission(x, 20)
    assert isinstance(result, str), \
        '''admission_functions.decide_admission should return a str, but returned {0}
           '''.format(type(result))
    assert result.strip().lower() in valid_strings, \
        '''admission_functions.decide_admission should return one of {0}, but returned {1}
           '''.format("'" + "', '".join(valid_strings) + "'", "'" + result + "'")


our_print("""
Hooray! The type checker passed!
This does NOT necessarily mean that your functions are correct!

It does mean that the functions in admission_functions.py:
- are named correctly,
- take the correct number of arguments, and
- return the correct types.

Be sure to thoroughly test your functions yourself before submitting.""")

builtins.print = our_print
builtins.input = our_input
