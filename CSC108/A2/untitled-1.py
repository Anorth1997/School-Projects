def palindrome1(x):
    return x == x[::-1]

def palindrome2(x):
    if len(x) % 2 == 0:
        return x[: len(x) // 2] == x[len(x) // 2:][::-1]
    else:
        return x[: len(x) // 2] == x[len(x) // 2 + 1 :][::-1]

def palindrome3(x):
    for  i in range(len(x)):
        while i < len(x) / 2 and x[i] != x[(len(x) - i - 1)]:
            return False
    return True

