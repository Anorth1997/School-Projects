import admission_functions as af

# Format of a student record
# name,school,gradyear,course1,grade1,exam1,course2,grade2,exam2,course3,grade3,exam3,degree

# NOTE: For A1, lines containing student records can exceed 80 characters.
# All other lines must stay under the 80 character limit.

NAME_INDEX = 0
TRANSCRIPT_INDEX = 3
NUM_APPLICATION_COURSES = 3
MARK_LENGTH = 2


def process_student_records(records):
    """ (list of str) -> NoneType

    Main function for processing application records in the admission system.
    """

    for record in records:
        record_data = record.split(',')
        transcript = ','.join(record_data[TRANSCRIPT_INDEX:-1])

        mark_list = get_marks(record, transcript)
        determine_degree_admission(record, record_data[NAME_INDEX], mark_list)


def get_marks(record, transcript):
    """ (str, str) -> list of float

    Return a list of final course marks from transcript that can be used for
    admission, computed based on information in record.

    >>> record = 'Eyal de Lara,Fort McMurray Composite High,2016,MAT,90,92,ENG,92,NE,BIO,77,85,BSci'
    >>> transcript = 'MAT,90,92,ENG,92,NE,BIO,77,85'
    >>> get_marks(record, transcript)
    [91.0, 92.0, 81.0]
    >>> record = 'Paul Gries,Ithaca High School,1986,BIO,61,70,CHM,80,90,CAT,95,96,BEng'
    >>> transcript = 'BIO,61,70,CHM,80,90,CAT,95,96'
    >>> get_marks(record, transcript)
    [65.5, 85.0]
    """
    
    valid_admission_courses = ['BIO', 'CHM', 'ENG', 'MAT', 'SCI']
    mark_list = []

    for i in range(1, NUM_APPLICATION_COURSES + 1):
        course = af.extract_course(transcript, i)
        for course_code in valid_admission_courses:
            both_marks = af.get_both_marks(course, course_code)
            if len(both_marks) > 0:
                course_mark = both_marks[:MARK_LENGTH]
                exam_mark = both_marks[MARK_LENGTH + 1:]
                final_mark = af.get_final_mark(record, course_mark, exam_mark)
                mark_list.append(final_mark)
    return mark_list


def determine_degree_admission(record, name, mark_list):
    """ (str, str, list of float) -> NoneType

    Prints the admission decision for each record containing name and the
    decision based on the average of mark_list.

    >>> record = 'Jacqueline Smith,Grande Prairie Composite High,2016,MAT,90,94,ENG,92,88,CHM,80,85,BArts'
    >>> name = 'Jacqueline Smith'
    >>> determine_degree_admission(record, name, [92.0, 90.0, 82.5])
    BArts admission decision for Jacqueline Smith: accept with scholarship
    >>> record = 'Paul Gries,Ithaca High School,1986,BIO,60,70,CHM,80,90,CAT,95,96,BEng'
    >>> determine_degree_admission(record, 'Paul Gries', [65.0, 85.0])
    BEng admission decision for Paul Gries: reject
    """

    degrees = {'BArts': 80, 'BCom': 82, 'BEng': 84, 'BMusic': 86, 'BSci': 88}

    for degree in degrees:
        if af.applied_to_degree(record, degree):
            average = sum(mark_list) / NUM_APPLICATION_COURSES
            cutoff = degrees[degree]
            decision = af.decide_admission(average, cutoff)
            print('{0} admission decision for {1}: {2}'.format(degree, name,
                                                               decision))


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    records_string = \
        '''Jacqueline Smith,Best High School,2002,MAT,90,94,ENG,92,88,CHM,80,85,BArts
Eyal de Lara,Fort McMurray Composite High,2016,MAT,90,92,ENG,92,NE,BIO,77,85,BSci
Paul Gries,Ithaca High School,1986,BIO,60,70,CHM,80,90,CAT,95,96,BEng
Andrew Petersen,Some Other High School,2016,BIO,83,86,MAT,91,84,SCI,95,77,BMusic
Jen Campbell,Yet Another High School,2015,ENG,75,78,SCI,80,81,CHM,80,81,BCom'''

    records = records_string.split('\n')
    process_student_records(records)
