'''restrictive_growth_strings.py: Constructs the lexicographic
 restrictive growth string representation of all the way to partition a set,
 given the length of the set.'''

__author__ = "Justin Overstreet"
__copyright__ = "oversj96.github.io"


def set_to_zero(working_set, index):
    '''Given a set and an index, set all elements to 0 after the index.'''
    if index == len(working_set) - 1:
        return working_set
    else:
        for i in range(index + 1, len(working_set)):
            working_set[i] = 0
        return working_set


def update_b_row(a_row, b_row):
    '''Update b row to reflect the max value of a sequence range in row a'''
    for i in range(1, len(a_row)):
        b_row[i-1] = max(a_row[:i]) + 1
    return b_row


def restrictive_growth_strings(length):   
    '''Returns the set of all partitions of a set in a lexicographic integer format.
    The algorithm is based on Donald Knuth's volume 4A on combinatoric algorithms.
    Algorithm H.'''
    n = length - 1
    a_string = [0 for i in range(0, length)]
    b_string = [1 for i in range(0, n)]
    lexico_string = [a_string.copy()]
    incrementable = True   
    while incrementable:
        incrementable = False
        for index in range(n, 0, -1):           
            if a_string[index] < n and a_string[index] < b_string[index - 1]:
                incrementable = True
                a_string[index] += 1
                a_string = set_to_zero(a_string, index)
                b_string = update_b_row(a_string, b_string)
                lexico_string.append(a_string.copy())
                break      
    return lexico_string


if __name__ == "__main__":
    '''A quick way to check if the module works correctly is to compare
    the partition count to the bell number of the correct 'n' size.
    For a set of 7 elements, the partition count should be 877 by Bell's numbers.'''
    strings = restrictive_growth_strings(4)
    for string in strings:
        print(string)
    print(len(strings))