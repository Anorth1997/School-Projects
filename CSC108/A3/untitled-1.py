candidates = ['Donald Trump', 'Governor Gary Johnson', 'Secretary Hillary Clinton', 'Dr. Jill Stein']

def delist_to_str(the_list):
    x = ''
    for item in the_list:
        x = x + item
    return x

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
    
    for line in file:
        if line[:-2] in candidates:
            candidate = line[:-2]
            result[candidate] = []
        
    
        elif line != '<<<EOT\n':
            tweet.append(line)
        else:
            tweet_history = tweet[0].split(',')
            tup = (candidate, delist_to_str(tweet[1:]), tweet_history[1], tweet_history[3], tweet_history[4], tweet_history[5][:-1])
            result[candidate].append(tup)
            tweet = []
        
    return result
    
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

def clean_str_in_list(uncleaned_list):
    """ (list of str) -> list of str
    
    Precondiction: uncleaned_list is the output of the function extract_mentions
    or extract_hashtags.
    
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

def invert_dictionary(word_d):
    """ (dict of {str: int}, int) -> dict of {int: list of str}, int
    
    Return a dictionary which is the inverted version of word_d. This is a 
    helper function of common_words.
    
    >>> inverted = invert_dictionary({'you': 2, 'dont': 1, 'wish': 1, \
    'could': 1, 'vote': 1, 'have': 2})
    >>> inverted == {2: ['you', 'have'], 1: ['dont', 'vote', 'could', 'wish']}
    True
    """
    
    inverted_dictionary = {}
    for word in word_d:
        num = word_d[word]
        
        if not (num in inverted_dictionary):
            inverted_dictionary[num] = [word]
        else:
            inverted_dictionary[num].append(word)
    
    return inverted_dictionary

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
    
    new_word_d = invert_dictionary(word_d)
    
    new_word_d_keys = []
    for num in new_word_d:
        new_word_d_keys.append(num)
    
    if len(new_word_d_keys) != 0:
        largest = max(new_word_d_keys)
        
        n = 0
        
        for count in new_word_d_keys:
            h = len(new_word_d[count])
            n = h + n
            if n < N:
                
                
            
        
    
         
    



if __name__ == '__main__':
    file = open('short_data.txt')
    x = read_tweets(file)
    import doctest
    doctest.testmod()
    