candidates = ['Donald Trump', 'Governor Gary Johnson', \
              'Secretary Hillary Clinton', 'Dr. Jill Stein']
tie = 'Tie'
unknown = 'Unknown'

def clean_str_in_list(uncleaned_list):
    """ (list of str) -> list of str
    
    Precondiction: uncleaned_list is helper function of the function 
    extract_mentions or extract_hashtags.
    
    Return a cleaned list of str, which the str in the list contains only 
    alphanumeric characters.
    
    >>> clean_str_in_list(['@dd,d'])
    ['dd']
    >>> clean_str_in_list(['@', '@', '@', '@cat,'])
    ['', '', '', 'cat']
    """
    
    
    for i in range(len(uncleaned_list)):
        cleaned = ''
        j = 1
        while j < len(uncleaned_list[i]) and uncleaned_list[i][j].isalnum():
            cleaned += uncleaned_list[i][j]
            j += 1
        
        uncleaned_list[i] = cleaned
    
    return uncleaned_list

def extract_mentions(text):
    """ (str) -> list of str
    
    Precondiction: The text has to be in form of a tweet text. 1 <= len(text),
    len(text) <= 140.
    
    Return a list containing all of the mentions in the text, in the order they 
    appear in the text without the mention symbol. Return an empty list if no 
    mentions in text.
    
    >>> extract_mentions("__@lll, @dd,d dafsd")
    ['dd']
    >>> extract_mentions("__@lll, @ @ @ ")
    ['', '', '']
    >>> extract_mentions("@CAT, @CAT @cat")
    ['CAT', 'CAT', 'cat']
    """
    
    result = []
    
    text_list = text.split()
    for item in text_list:
        if item.startswith('@'):
            result.append(item)
    
    return clean_str_in_list(result)

def extract_hashtags(text):
    """ (str) -> list of str
    
    Precondiction: The text has to be in form of a tweet text. 1 <= len(text),
    len(text) <= 140.
    
    Return a list containing all of the hashtags in the text, in the order they 
    appear in the text without the hashtags symbol. Return an empty list if no 
    hashtags in text. One hashtag only appear once in the returned list.
    
    >>> extract_hashtags("__#lll, #dd,d dasfads")
    ['dd']
    >>> extract_hashtags("__#lll, # # # ")
    ['']
    >>> extract_hashtags("__#lll, #CAT, #CAT #cat")
    ['CAT']
    """
    
    hashtag_list = []
        
    text_list = text.split()
    for item in text_list:
        if item.startswith('#'):
            hashtag_list.append(item)       
    
    cleaned_list = clean_str_in_list(hashtag_list)
    
    result = []
    compare = []
    for item in cleaned_list:
        if not item.lower() in compare:
            compare.append(item.lower())
            result.append(item)
            
    return result

def get_cleaned_words(words_list):
    """  (list of str) -> (list of str)
    
    Precondiction: The word_list is the helper function of the function count
    words.
    
    Return a cleaned words list which each elements is a str that contains 
    numers and lower case alphabetic characters only.
    
    >>> get_cleaned_words(["Don't", 'you', 'wish', 'you', 'could', 'vote?'])
    ['dont', 'you', 'wish', 'you', 'could', 'vote']
    
    >>> get_cleaned_words([',,,', '???', '?ye?e', 'Tomorrow'])
    ['yee', 'tomorrow']
    """
    
    result = []
    
    for i in range(len(words_list)):
        words_list[i] = words_list[i].lower()
    
    for i in range(len(words_list)):
        word = ''
        for ch in words_list[i]:
            if ch.isalnum():
                word = word + ch
        if word != '':
            result.append(word)
    
    return result
            
def count_words(text, word_d):
    """ (str, dict of {str: int}) -> NoneType
    
    Precondiction: The text has to be in form of a tweet text. 1 <= len(text),
    len(text) <= 140.
    
    Update the counts of words in the dictiondary. If a word is not in the 
    dictionary yet, it should be added.
    
    >>> word_d = {}
    >>> count_words("@utmandrew Don't you wish you could vote? \
    #MakeAmericaGreatAgain", word_d)
    >>> word_d == {'you': 2, 'dont': 1, 'wish': 1, 'could': 1, 'vote': 1}
    True
    
    >>> word_d = {'you': 1, 'dont': 2, 'have': 2}
    >>> count_words("@utmandrew Don't you wish you could vote? \
    #MakeAmericaGreatAgain", word_d)
    >>> word_d == {'you': 3, 'have': 2, 'could': 1, 'wish': 1, 'dont': 3, \
    'vote': 1}
    True
    """
    
    new_text = text.split()
    words = []
    
    for item in new_text:
        if not (item.startswith('@') or item.startswith('#') or \
           item.startswith('http://')):
            words.append(item)
    
    cleaned_words = get_cleaned_words(words)
    
    for item in cleaned_words:
        if item in word_d:
            word_d[item] = word_d[item] + 1
        elif not item in word_d:
            word_d[item] = 1

def common_words(word_d, N):
    """ (dict of {str: int}, int) -> None
    
    Precondiction: N is an integer.
    
    This function should update the dictionary so that it includes the most 
    common (highest frequency words). At most N words should be included in 
    the dictionary. 
    
    >>> word_d = {'you': 2, 'dont': 1, 'wish': 1, 'could': 1, 'vote': 1, \
    'have': 2}
    >>> common_words(word_d, 3)
    >>> word_d == {'you': 2, 'have': 2}
    True
    
    >>> word_d = {'you': 2, 'dont': 1, 'wish': 1, 'could': 1, 'vote': 1, \
    'have': 3}
    >>> common_words(word_d, 1)
    >>> word_d == {'have': 3}
    True
    
    """
    
    if N <= len(word_d):
    
        word_d_duplicate = {}
        for item in word_d:
            word_d_duplicate[item] = word_d[item]
        word_d.clear()
        storage = []
        for item in word_d_duplicate:
            storage.append((item, word_d_duplicate[item]))
        storage_count = []
        for item in storage:
            storage_count.append(item[1])
        storage_count_duplicate = []
        for num in storage_count:
            storage_count_duplicate.append(num)
    
        n = 0
        indecies = []
        while n < N:

            largest = max(storage_count_duplicate)
            h = storage_count_duplicate.count(largest)
            n = n + h
            if n <= N:
                indecies = indecies + find_indecies(storage_count, largest)
                for num in storage_count_duplicate:
                    if num == largest:
                        storage_count_duplicate.remove(num)
    
        for index in indecies:
            word_d[storage[index][0]] = storage[index][1]
            
                

def find_indecies(nums, I):
    """ (list of ints, int) -> list in ints
    
    Return the indecies of the I in the nums.
    
    >>> find_indecies([3, 3, 2, 2, 1], 3)
    [0, 1]
    >>> find_indecies([4, 5, 6, 7], 7)
    [3]
    """
    
    result = []
    
    for i in range(len(nums)):
        if nums[i] == I:
            result.append(i)
    return result



def delist_to_str(the_list):
    """ (list of str) -> str
    
    Return a str that is combined by all the elements in the_list by order 
    (break down the_list and stick them to form a str). This is a helper 
    function.

    >>> delist_to_str(['a','b','c',''])
    'abc'
    >>> delist_to_str(['a','b',' '])
    'ab '
    """
    string = ''
    for item in the_list:
        string = string + item
    return string


def read_tweets(tweet_file):
    """ (file open for reading) -> dict of {str: list of tweet tuples}
    
    Precondiction: tweet_file has to be a data file containing tweets.
    
    Return a dictionary that its keys should be the names of the candidates in 
    form of string, and the items in the list associated with each candidate are
    the tweets in form of tuples they have sent. A tweet tuple should have the 
    form (candidate, tweet text, date, source, favorite count, retweet count).
      
    """
    
    result = {}
    tweet = []
    
    for line in tweet_file:
        if line[:-2] in candidates:
            candidate = line[:-2]
            result[candidate] = []
        
        elif line != '<<<EOT\n':
            tweet.append(line)
            
        else:
            tweet_history = tweet[0].split(',')
            tup = (candidate, delist_to_str(tweet[1:]), tweet_history[1], \
                   tweet_history[3], tweet_history[4], tweet_history[5][:-1])
            result[candidate].append(tup)
            tweet = []
        
    return result


def most_popular(tweet_d, date_start, date_end):
    """ (dict of {str: list of tweet tuples}, int, int) -> str
    
    Precondiction: date_start <= date_end, tweet_d is the output of the function
    read_tweets. date_start >= 0 and date_end >= 0.
    
    This function should return which candidate was the most popular on Twitter 
    between the date_start and date_end(inclusive). A candidate's 
    popularity in a time period is the sum of the favorite counts and retweet 
    counts for all tweets issued in that time period. In the case of a tie,
    return the string "Tie".

    >>> most_popular({'candidate1':[('candidate1', 'tweet_text_1', '1005', \
    'source1', '1', '1'), ('candidate1', 'tweet_text_2', '1006', 'source1', \
    '2', '1')],'candidate2':[('candidate2', 'tweet_text_3', '1003', 'source1', \
    '1', '0'), ('candidate2', 'tweet_text_4', '1105', 'source1', '1', '1')]}, \
    1001, 1229)
    'candidate1'
    >>> most_popular({'candidate1':[('candidate1', 'tweet_text_1', '1005', \
    'source1', '1', '1'), ('candidate1', 'tweet_text_2', '1006', 'source1', \
    '2', '1')],'candidate2':[('candidate2', 'tweet_text_3', '1003', 'source1', \
    '2', '1'), ('candidate2', 'tweet_text_4', '1105', 'source1', '1', '1')]}, \
    1001, 1229)
    'Tie'
    """

    popular_dictionary = {}

    for candidate in tweet_d:
        popular_dictionary[candidate] = 0
        for tweet in tweet_d[candidate]:
            if date_start <= int(tweet[2]) <= date_end:
                popular_dictionary[candidate] = popular_dictionary[candidate] \
                    + int(tweet[4]) + int(tweet[5])
    
    common_words(popular_dictionary, 1)
    if len(popular_dictionary) == 1:
        for key in popular_dictionary:
            return key
    else:
        return tie



def hashtags_for_candidates(tweet_d):
    """ (dict of {str: list of tweet tuples}) -> dict of {str: list of str})
    
    Precondiction: tweet_d is the output of the function read_tweets.
    
    Return a dictionary which the keys are the name of candidates, and their
    values are all the hashtags in the tweets related to them.

    >>> hash_dict = hashtags_for_candidates({'candidate1':[('candidate1', \
    'blahblahblah #DTDT', '1005', 'source1', '1', '1'), ('candidate1', \
    'AAAA #A', '1006', 'source1', '2', '1')],'candidate2':[('candidate2', \
    'ABCD #A #B', '1003', 'source1', '1', '0'), ('candidate2', '#Hellooooooo', \
    '1105', 'source1', '1', '1')]})
    >>> hash_dict == {'candidate1': ['DTDT', 'A'], 'candidate2': ['A', 'B', \
    'Hellooooooo']}
    True
    """
    
    result = {}
    
    for candidate in tweet_d:
        result[candidate] = []
        for tweet in tweet_d[candidate]:
            result[candidate] += extract_hashtags(tweet[1])
    
    return result

def unique_hashtags(hashtags_d):
    """ (dict of {str: list of str}) -> dict of {str: list of str}
    
    Precondiction: hashtag_d is the output of the function 
    hashtags_for_candidates.
    
    Return a dictionary which the keys are the name of candidates, and their
    values are all the unique hashtags in the tweets related to them.

    >>> hash_unique = unique_hashtags({'candidate1': ['DTDT', 'A'], \
    'candidate2': ['A', 'B', 'Hellooooooo']})
    >>> hash_unique == {'candidate1': ['DTDT'], 'candidate2': ['B', \
    'Hellooooooo']}
    True
    
    >>> hash_unique = unique_hashtags({'candidate1': ['A'], \
    'candidate2': ['A', 'B', 'Hellooooooo']})
    >>> hash_unique == {'candidate1': [], 'candidate2': ['B', 'Hellooooooo']}
    True
    """

    result = {}
    hashtag_counts = {}  
    for candidate in hashtags_d:
        for hashtag in hashtags_d[candidate]:
            count_words(hashtag, hashtag_counts)
    
    removed = []
    for item in hashtag_counts:
        if hashtag_counts[item] != 1:
            removed.append(item)
               
    for candidate in hashtags_d:
        keep = []
        for hashtag in hashtags_d[candidate]:
            if not hashtag.lower() in removed:
                keep.append(hashtag)
        result[candidate] = []        
        for hashtag_keep in keep:
            result[candidate].append(hashtag_keep) 
        
    return result
        
    
def detect_author(tweet_d, text):
    """ (dict of {str: list of tweet tuples}, str) -> str
    
    Precondiction: tweet_d is the output of function read_tweets, and text is 
    a formal tweet text.
    
    Return the author of the text by evaluating the hashtags used in the text;
    if there are hashtags used by two or more candidates or no hashtags used 
    in text, return 'Unknown'.

    >>> detect_author({'candidate1':[('candidate1', 'blahblahblah #DTDT', \
    '1005', 'source1', '1', '1'), ('candidate1', 'AAAA #A', '1006', 'source1', \
    '2', '1')],'candidate2':[('candidate2', 'ABCD #A #B', '1003', 'source1', \
    '1', '0') , ('candidate2', '#Hellooooooo', '1105', 'source1', '1', '1')]}, \
    'ABABCCDD #A')
    'Unknown'
    >>> detect_author({'candidate1':[('candidate1', 'blahblahblah #DTDT', \
    '1005', 'source1', '1', '1'), ('candidate1', 'AAAA #A', '1006', 'source1', \
    '2', '1')],'candidate2':[('candidate2', 'ABCD #A #B', '1003', 'source1', \
    '1', '0'), ('candidate2', '#Hellooooooo', '1105', 'source1', '1', '1')]}, \
    'ABABCCDD #B')
    'candidate2'
    >>> detect_author({'candidate1':[('candidate1', 'blahblahblah #DTDT', \
    '1005', 'source1', '1', '1'), ('candidate1', 'AAAA #A', '1006', 'source1', \
    '2', '1')],'candidate2':[('candidate2', 'ABCD #A #B', '1003', 'source1', \
    '1', '0'), ('candidate2', '#Hellooooooo', '1105', 'source1', '1', '1')]}, \
    'ABABCCDD')
    'Unknown'
    """
    
    unique = unique_hashtags(hashtags_for_candidates(tweet_d))
    used_hashtags = extract_hashtags(text)
    
    test_unique = {}
    for hashtag in used_hashtags:
        for candidate in unique:
            test_unique[candidate] = []
            if hashtag in unique[candidate]:
                test_unique[candidate] += [hashtag]
    
    counter = 0
    for unique_list in test_unique:
        if len(test_unique[unique_list]) != 0:
            counter += 1
            author = unique_list
            
    if counter != 1:
        return unknown
    else:
        return author
    
if __name__ == '__main__':  
    import doctest
    doctest.testmod()