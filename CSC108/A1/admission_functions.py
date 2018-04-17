SPECIAL_CASE_SCHOOL_1 = 'Fort McMurray Composite High'
SPECIAL_CASE_SCHOOL_2 = 'Father Mercredi High School'
SPECIAL_CASE_YEAR = '2016'
SPECIAL_CASE_EXAM = 'NE'



def is_special_case(record):
    """ (str) -> bool

    Return True iff the student represented by record is a special case.

    >>> is_special_case('Jacqueline Smith,Fort McMurray Composite High,2016,MAT,90,94,ENG,92,88,CHM,80,85,BArts')
    True
    >>> is_special_case('Jacqueline Smith,Father Something High School,2016,MAT,90,94,ENG,92,88,CHM,80,85,BArts')
    False
    >>> is_special_case('Jacqueline Smith,Fort McMurray Composite High,2015,MAT,90,94,ENG,92,88,CHM,80,85,BArts')
    False
    """
    
    special_case_status = (SPECIAL_CASE_SCHOOL_1 in record or SPECIAL_CASE_SCHOOL_2 in record) and SPECIAL_CASE_YEAR in record
    return special_case_status


def get_final_mark(record, mark_coursework, mark_exam):
    """ (str, str, str) -> float

    Precondition: len(mark_coursework) = 2 and len(mark_exam) = 2
    
    Return the final mark of a particular course by calculating the average of grade of courseword and exam.
    
    >>>get_final_mark('Jacqueline Smith,Fort McMurray Composite High,2016,MAT,90,94,ENG,92,88,CHM,80,85,BArts', '90', '94')
    92.0
    >>>get_final_mark('Jacqueline Smith,Fort McMurray Composite High,2016,MAT,90,94,ENG,92,88,CHM,80,85,BArts', '92', '88')
    90.0
    """
    
    if is_special_case(record) == True:
        if SPECIAL_CASE_EXAM in mark_exam:
            return float(mark_coursework) 
        else:
            return (float(mark_coursework) + float(mark_exam)) / 2
    if is_special_case(record) == False:
        if SPECIAL_CASE_EXAM in mark_exam:
            return float(mark_coursework) / 2
        else:
            return (float(mark_coursework) + float(mark_exam)) / 2

def get_both_marks(course, course_code):
    """ (str, str) -> str

    Return the coursework mark and exam mark from the given course record and course code if the given variables match; else, return an empty string.
    
    >>>get_both_marks('MAT,90,94', 'MAT')
    '90 94'
    >>>get_both_marks('MAT,90,92', 'ENG')
    ''
    """
    
    if course_code in course:
        return course[4:6] + ' ' + course[7:9]
    else:
        return ''

def extract_course(transcript, wanted_course):
    """ (str, int) -> str
    
    Precondiction: wanted_course can only be taken as 1, 2 or 3.
    
    Return the course record of a particular course from a student's transcript and the wanted course.
    
    >>>extract_course('MAT,90,94,ENG,92,88,CHM,80,85', 2)
    'ENG,92,88'
    >>>extract_course('MAT,85,99,ENG,93,86,CHM,94,95', 3)
    'CHM,94,95'
    """
    
    
    return transcript[(wanted_course - 1) * 10:9 + (wanted_course - 1) * 10]

def applied_to_degree(record, degree):
    """ (str, str) -> bool
    
    Return a boolean tells that if the student record which is represented in the first parameter applies to the degree which is represented by the second parameter.
    
    >>>applied_to_degree("Jacqueline Smith,Best High School,2002,MAT,90,94,ENG,92,88,CHM,80,85,BArts", "BArts")
    True
    >>>applied_to_degree("Eyal de Lara,Fort McMurray Composite High,2016,MAT,90,92,ENG,92,NE,BIO,77,85,BSci", "BSci")
    True
    """
    
    return degree in record[-7:]

def decide_admission(average, cutoff):
    """ (number, number) -> str
    
    Return the adimission decision by comparing the student's average mark and cutoff mark.
    
    >>>decide_admission(85, 80)
    'accept with scholarship'
    >>>decide_admission(70, 80)
    'reject'
    """
    
    if average < cutoff:
        return 'reject'
    elif average >= cutoff + 5:
        return 'accept with scholarship'
    else:
        return 'accept'